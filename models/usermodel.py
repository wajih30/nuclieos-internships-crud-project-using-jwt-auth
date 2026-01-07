from sqlalchemy import Column, Integer, String , DateTime, func

from db.db import base


class Users(base):
    __tablename__= "Users"

    id=Column(Integer,primary_key=True, index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    role=Column(String,nullable=False)
    password=Column(String,nullable=False)
    created_at= Column(DateTime(timezone=True), server_default=func.now())


