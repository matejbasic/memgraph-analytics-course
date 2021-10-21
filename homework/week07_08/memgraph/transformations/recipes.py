import mgp
import json


@mgp.transformation
def transaction(messages: mgp.Messages) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    print("start")
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        recipe = json.loads(message.payload().decode("utf8"))

        print(recipe)

        result_queries.append(mgp.Record(query="MERGE (:Recipe {name: $name})", parameters={"name": recipe["title"]}))

        result_queries += [
            mgp.Record(query="MERGE (:Tag {name: $name})", parameters={"name": x}) for x in recipe["tags"]
        ]
        result_queries += [
            mgp.Record(query="MERGE (:Ingredient {name: $name})", parameters={"name": x}) for x in recipe["ingredients"]
        ]

        for ingredient in recipe["ingredients"]:
            result_queries.append(mgp.Record(
                query=("MATCH (r:Recipe {name: $recipe_name}), (i:Ingredient {name: $ingredient_name}) "
                       "CREATE (r)-[:USING]->(i)"),
                parameters={"recipe_name": recipe["title"], "ingredient_name": ingredient}
            ))

        for tag in recipe["tags"]:
            result_queries.append(mgp.Record(
                query=("MATCH (r:Recipe {name: $recipe_name}), (t:Tag {name: $tag_name}) "
                       "CREATE (r)-[:TAGGED]->(t)"),
                parameters={"recipe_name": recipe["title"], "tag_name": tag}
            ))

    return result_queries
