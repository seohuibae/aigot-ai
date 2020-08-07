import peewee 
from peewee import *

from scipy.stats import norm
import math

db1 = peewee.SqliteDatabase('test.db')

class UniversityDB(peewee.Model):
    
    university = peewee.TextField() # '서울대학교', ...
    category = peewee.TextField() # '일반', '기회균등', ...
    department = peewee.TextField() # '자연', ...
    major = peewee.TextField() # '물리학과', ...
    valmin = peewee.DoubleField() # '2.73', ...
    
    class Meta: 
        database = db1


def retrieve_probability(university, category, department, major, myval):
    uni = UniversityDB.select().where(UniversityDB.university == university and UniversityDB.category == category and UniversityDB.department == department and UniversityDB.major == major).get()
    mu = uni.valmin 
    std = abs(1-mu)/3
    probability = (1 - norm.cdf(myval, mu, std)) * 100
    if probability > 95.0: probability = 95.0

    return probability

if __name__ == "__main__":

    st = StudentDB.select().where(StudentDB.id == 0x01).get() # TODO correct id 
    retrieve_probability(st.university, st.category, st.department, st.major, st.myval) 
