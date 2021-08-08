from typing import Dict, Any

RawRecipeType = Dict[str, Any]


def is_low_fat(raw_recipe: RawRecipeType) -> bool:
    return raw_recipe["fat"] <= 3.0 if isinstance(raw_recipe["fat"], (float, int)) else True


def is_high_fat(raw_recipe: RawRecipeType) -> bool:
    return raw_recipe["fat"] > 17.5 if isinstance(raw_recipe["fat"], (float, int)) else False


def is_low_calorie(raw_recipe: RawRecipeType) -> bool:
    return raw_recipe["calories"] <= 40.0 if isinstance(raw_recipe["calories"], (float, int)) else True


def is_high_calorie(raw_recipe: RawRecipeType) -> bool:
    return raw_recipe["calories"] > 800.0 if isinstance(raw_recipe["calories"], (float, int)) else False


def is_low_protein(raw_recipe: RawRecipeType) -> bool:
    return raw_recipe["protein"] <= 5.0 if isinstance(raw_recipe["protein"], (float, int)) else True


def is_high_protein(raw_recipe: RawRecipeType) -> bool:
    return raw_recipe["protein"] > 50.0 if isinstance(raw_recipe["protein"], (float, int)) else False


def is_low_salt(raw_recipe: RawRecipeType) -> bool:
    return raw_recipe["sodium"] <= 1.0 if isinstance(raw_recipe["sodium"], (float, int)) else True


def is_high_salt(raw_recipe: RawRecipeType) -> bool:
    return raw_recipe["sodium"] > 400.0 if isinstance(raw_recipe["sodium"], (float, int)) else False
