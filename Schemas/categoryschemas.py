from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class CategoryBase(BaseModel):
    CategoryName : str




class CategoryUpdate(BaseModel):
    CategoryName: Optional[str] = None




class CategoryResponse(CategoryBase):
    CategoryId: int
    created_at: datetime 

    class Config:
        orm_mode= True






