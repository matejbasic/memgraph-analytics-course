import random
from graph_db import memgraph

from logger import log_time, log

POS_COUNT = 10
COMPROMISED_POS_COUNT = 2

CARDS_COUNT = 20

TRANSACTIONS_COUNT = 30
FRAUDULENT_TRANSACTIONS_RATE = 0.1


@log_time
def create_cards_and_pos(cards_count: int, pos_count: int):
    memgraph.execute(f"UNWIND range(0, {cards_count} - 1) AS id "
                     "CREATE (:Card {id: id, compromised: false})")

    memgraph.execute(f"UNWIND range({cards_count}, {cards_count + pos_count} - 1) AS id "
                     "CREATE (:Pos {id: id, compromised: false})")


@log_time
def compromise_pos_devices(cards_count: int, pos_count: int, compromised_pos_count: int):
    if compromised_pos_count > pos_count:
        compromised_pos_count = pos_count

    log.info(f"Compromising {compromised_pos_count} out of {pos_count} POS devices")

    compromised_devices = random.sample(range(cards_count, cards_count + pos_count), compromised_pos_count)
    for pos_id in compromised_devices:
        memgraph.execute(f"MATCH (p:Pos {{id: {pos_id}}}) SET p.compromised = true")
        log.info(f"Point of sale {pos_id} is compromised")


@log_time
def create_transactions(cards_count: int, pos_count: int, transactions_count: int, fraudulent_transactions_rate: float):
    log.info(f"Creating {transactions_count} transactions")

    query = ("MATCH (c:Card {{id: {card_id}}}), (p:Pos {{id: {pos_id}}}) "
             "CREATE (t:Transaction {{id: {transaction_id}, fraudReported: c.compromised AND (rand() < %f)}}) "
             "CREATE (c)<-[:USING]-(t)-[:AT]->(p) SET c.compromised = p.compromised" % fraudulent_transactions_rate)

    for i in range(cards_count + pos_count, cards_count + pos_count + transactions_count):
        card_id = random.randint(0, cards_count - 1)
        pos_id = random.randint(cards_count, cards_count + pos_count - 1)
        memgraph.execute(query.format(card_id=card_id, pos_id=pos_id, transaction_id=i))


@log_time
def generate_data():
    memgraph.drop_database()

    create_cards_and_pos(CARDS_COUNT, POS_COUNT)
    compromise_pos_devices(CARDS_COUNT, POS_COUNT, COMPROMISED_POS_COUNT)
    create_transactions(CARDS_COUNT, POS_COUNT, TRANSACTIONS_COUNT, FRAUDULENT_TRANSACTIONS_RATE)
