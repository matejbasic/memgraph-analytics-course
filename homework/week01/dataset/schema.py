from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Recipe:
    __slots__ = ["title", "ingredients"]
    title: str
    ingredients: List[str]
