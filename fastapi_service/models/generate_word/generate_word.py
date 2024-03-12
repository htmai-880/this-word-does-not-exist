from pydantic import BaseModel
from typing import Optional
from ..word_definition import WordDefinition

# Response
class GenerateWordResponse(BaseModel):
    word: WordDefinition
