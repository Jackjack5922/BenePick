from pydantic import BaseModel
from typing import Optional

class UserInput(BaseModel):
    나이: int
    성별: str
    소득구간: str
    출산여부: Optional[bool] = False
    지역: Optional[str] = ""