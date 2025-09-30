from pydantic import BaseModel
from typing import List

class ParentSegmentMapping(BaseModel):
    parent_text_id: str
    segments: List[str]

class TextMapping(BaseModel):
    text_id: str
    segment_id: str
    mappings: List[ParentSegmentMapping]

class Mapping(BaseModel):
    text_mappings: List[TextMapping]