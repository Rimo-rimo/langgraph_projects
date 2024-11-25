from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from typing import Optional


# Pydantic

class Section(BaseModel):
    section_title: str = Field(..., title="The title of the section in research note")
    contents: str = Field(..., title="The content of the section")

class DraftOutline(BaseModel):
    """연구노트 작성을 위한 초안"""
    title: str = Field(..., title="The title of the research note")
    sections: list[Section] = Field(..., title="The sections in the research note")