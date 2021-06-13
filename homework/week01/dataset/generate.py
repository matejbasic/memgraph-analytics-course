import json
import re

import numpy as np

import dataset

INGREDIENTS_BLACKLIST = [
    "chopped", "sliced", "leaves", "a", "imported", "temperature", "accompaniment", "blend", "dry", "fresh",
    "vegetables",
]


def load_raw_data():
    processed_ingredients = np.load("raw/ingredients.npy")
    with open("raw/full_format_recipes.json") as f:
        recipes = json.load(f)
    return processed_ingredients, recipes


def find_ingredient(processed_ingredients, ingredient_raw):
    try:
        return max([
            ingredient
            for ingredient in processed_ingredients
            if ingredient not in INGREDIENTS_BLACKLIST and re.search(rf"\b{ingredient}\b", ingredient_raw)
        ], key=len)
    except ValueError:
        return None


def get_ingredients(processed_ingredients, recipe_ingredients):
    return list(filter(None, {
        find_ingredient(processed_ingredients, ingredient_raw.lower())
        for ingredient_raw in recipe_ingredients
    }))


def get_processed_recipes(max_recipes_count=100):
    processed_ingredients, recipes = load_raw_data()
    for recipe in recipes[:max_recipes_count]:
        if recipe.get("title") and recipe.get("ingredients"):
            title = recipe["title"]
            recipe_ingredients = get_ingredients(processed_ingredients, recipe["ingredients"])
            yield title, recipe_ingredients


if __name__ == "__main__":
    recipes = [
        {"title": recipe_title, "ingredients": ingredients}
        for recipe_title, ingredients in get_processed_recipes()
    ]
    dataset.save(recipes)
