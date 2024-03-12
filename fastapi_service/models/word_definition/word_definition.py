from pydantic import BaseModel
from ..dataset import DatasetType
from typing import Optional

class WordDefinition(BaseModel):
    word: str
    definition: str
    pos: str
    examples: list[str] = []
    syllables: list[str] = []
    probablyExists: bool = False
    dataset: Optional[DatasetType] = DatasetType(name="OED")