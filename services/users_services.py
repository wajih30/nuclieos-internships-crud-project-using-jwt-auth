from sqlalchemy.orm import Session
from models import usermodel
from Schemas import userschemas

class User():
    def __init__(self,db:Session):
        self.db=db

    def create_user(self,user_name,user_email,user_role):
        db_user = usermodel.Users(name=user_name, email=user_email,role=user_role)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def read_user(self):
        return self.db.query(usermodel.Users).all()
    
    def read_user_by_id(self,user_id):
        return self.db.query(usermodel.Users).filter(usermodel.Users.id==user_id).first()
    
    def update_user(self,user_id: int,user_name:str, user_email:str,user_role:str):
        db_user = self.db.query(usermodel.Users).filter(usermodel.Users.id == user_id).first()
        if not db_user:
           return None

        db_user.name = user_name

        db_user.email = user_email
        db_user.role=user_role
        self.db.commit()
        self.db.refresh(db_user)
        return db_user    

    def delete_user(self,user_id):
        db_user = self.db.query(usermodel.Users).filter(usermodel.Users.id == user_id).first()
        if not db_user:
           return None
        self.db.delete(db_user)
        self.db.commit()
        return db_user






    

