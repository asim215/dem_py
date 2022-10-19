from peewee import Model, SqliteDatabase

database = SqliteDatabase("sqlite.db")

class BaseModel(Model):
    class Meta:
        database = database
        

from database.Users import UsersTable
from database.Users import PizzaTable
from database.Users import UsersTable

UsersTable.create_table()