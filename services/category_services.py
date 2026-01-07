from sqlalchemy.orm import Session
from models import categorymodel
from Schemas import categoryschemas

class Category():
    def __init__(self,db:Session):
        self.db=db

    def create_category(self,category_name:str):
        db_category = categorymodel.Category(CategoryName=category_name)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def read_category(self):
        return self.db.query(categorymodel.Category).all()
    
    def read_category_by_id(self,category_id:int):
        return self.db.query(categorymodel.Category).filter(categorymodel.Category.CategoryId==category_id).first()
    
    def update_category(self,category_id: int, category: categoryschemas.CategoryUpdate):
        db_category = self.db.query(categorymodel.Category).filter(categorymodel.Category.CategoryId==category_id).first()
        if not db_category:
           return None

        db_category.CategoryName = category.CategoryName
        self.db.commit()
        self.db.refresh(db_category)
        return db_category



    def delete_category(self,category_id:int):
        db_category = self.db.query(categorymodel.Category).filter(categorymodel.Category.CategoryId==category_id).first()

        if not db_category:
           return None
        self.db.delete(db_category)
        self.db.commit()
        return db_category








    

