from pydantic import BaseModel
from typing import Optional
from ..word_definition import WordDefinition
from ..dataset import DatasetType

# Request
class WordFromDefinitionRequest(BaseModel):
    definition: str
    do_sample: bool = False
    temperature: Optional[float] = None
    dataset: Optional[DatasetType] = DatasetType(name="OED")

# Response
class WordFromDefinitionResponse(BaseModel):
    word: WordDefinition