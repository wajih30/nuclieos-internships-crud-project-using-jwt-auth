from sqlalchemy import Column, Integer, String , DateTime, func

from db.db import base


class Category(base):
    __tablename__= "Category"

    CategoryId=Column(Integer,primary_key=True, index=True)
    CategoryName=Column(String,nullable=False,unique=True)
    created_at= Column(DateTime(timezone=True), server_default=func.now())
    


    



