import time
import os

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable

from .logger import log


KAFKA_HOST = os.getenv("KAFKA_HOST", "kafka")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")


def get_admin_client(stream_name: str) -> KafkaAdminClient:
    while True:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_HOST + ':' + KAFKA_PORT, client_id=stream_name)
            return admin_client
        except NoBrokersAvailable:
            log.error("Failed to connect to Kafka", exc_info=True)
            time.sleep(1)


def create_topic(stream_name: str, topic: str) -> None:
    admin_client = get_admin_client(stream_name)
    log.info("Connected to Kafka")

    topic_list = [NewTopic(name=topic, num_partitions=1, replication_factor=1)]

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except TopicAlreadyExistsError:
        pass

    log.info("Created topics")


def create_producer() -> KafkaProducer:
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_HOST + ':' + KAFKA_PORT)
            return producer
        except NoBrokersAvailable:
            log.info("Failed to connect to Kafka")
            time.sleep(1)
