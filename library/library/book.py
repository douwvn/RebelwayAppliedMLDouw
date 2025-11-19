from dataclasses import dataclass, field
from library.random_number_utils import RandomUtils

@dataclass(frozen=True, order=True, slots=True)
class Book:
    title: str
    author: str
    category: str
    subcategory: str
    id: str = field(default_factory=RandomUtils.generate_random_id)

    @property
    def search_string(self):
        return f"{self.title} {self.author} {self.category} {self.subcategory}"
