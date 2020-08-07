import peewee 
from peewee import *

# TODO: db address
db = peewee.SqliteDatabase('test.db')

class UniversityDB(peewee.Model):
    
    university = peewee.TextField() # '서울대학교', ...
    category = peewee.TextField() # '일반', '기회균등', ...
    department = peewee.TextField() # '자연', ...
    major = peewee.TextField() # '물리학과', ...
    valmin = peewee.DoubleField() # '2.73', ...
    
    class Meta: 
        database = db
    

    
UniversityDB.create_table()

# TODO : put data lists of all scripts under ../data/
data = [
    ... 
]

with db.atomic(): 
    query = UniversityDB.insert_many(data)
    query.execute()