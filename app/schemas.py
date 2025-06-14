from pydantic import BaseModel, Field
# from typing import Optional

class ItemBase(BaseModel):
    """Base schema for an Item."""
    name: str = Field(..., example="Pizza")
