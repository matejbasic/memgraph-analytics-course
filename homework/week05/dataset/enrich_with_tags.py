from typing import List, Dict, Any
import json

from . import tag_resolvers


ORIGINAL_DATASET_PATH: str = "processed_recipes.json"
ENRICHED_DATASET_PATH: str = "recipes_with_tags.json"
TAGS: List[str] = [
    "low_fat", "high_fat", "low_calorie", "high_calorie", "low_protein", "high_protein", "low_salt", "high_salt"
]

RecipeType = Dict[str, Any]


def save_recipes_with_tags(recipes: List[RecipeType]):
    with open(ENRICHED_DATASET_PATH, "w") as f:
        json.dump(recipes, f)


def get_processed_recipes() -> List[RecipeType]:
    with open(ORIGINAL_DATASET_PATH, "r") as f:
        return json.load(f)


def get_raw_recipes() -> Dict[str, RecipeType]:
    with open("raw/full_format_recipes.json") as f:
        raw_recipes = json.load(f)
    return {recipe["title"]: recipe for recipe in raw_recipes if "title" in recipe}


def is_tag_allowed(tag: str, raw_recipe: RecipeType) -> bool:
    resolver_name = f"is_{tag}"
    if hasattr(tag_resolvers, resolver_name):
        return getattr(tag_resolvers, resolver_name)(raw_recipe)
    return False


def get_tags(raw_recipe: RecipeType) -> List[str]:
    return [tag for tag in TAGS if is_tag_allowed(tag, raw_recipe)]


def main():
    raw_recipes = get_raw_recipes()
    recipes = get_processed_recipes()

    for recipe in recipes:
        raw_recipe = raw_recipes[recipe["title"]]
        recipe["tags"] = get_tags(raw_recipe)

    save_recipes_with_tags(recipes)


if __name__ == "__main__":
    main()
