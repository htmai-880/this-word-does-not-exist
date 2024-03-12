from pydantic import BaseModel
from ..dataset import DatasetType
from ..word_definition import WordDefinition
from typing import Optional


class DefineWordRequest(BaseModel):
    word: str
    dataset: DatasetType
    do_sample: bool = False
    temperature: Optional[float] = None
    dataset: Optional[DatasetType] = DatasetType(name="OED")

# Response
class DefineWordResponse(BaseModel):
    word: WordDefinition