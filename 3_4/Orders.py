from database import BaseModel
from peewee import *


class OrdersTable(BaseModel):
    orders_id = PrimaryKeyField(null=False)
    created = DateTimeField(
        constraints=[SQL("DEFAULT (datetime('now'))")]
    )
    user_id = ForeignKeyField(UsersTable)
    pizza_id = ForeignKeyField(PizzaTable)
    pizza_count = IntegerField()
    address = TextField()
    price = FloatField()
    status = TextField()
