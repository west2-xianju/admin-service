from pydantic import BaseModel, Field
from typing import Optional

class CreateAdminForm(BaseModel):
    username: str = Field(..., min_length=4, max_length=20)
    password: str = Field(..., min_length=6, max_length=20)
    level: str = Field(..., regex='^(superuser|admin)$')
    
    
class UpdateAdminForm(BaseModel):
    username: Optional[str]
    level: Optional[str]
    