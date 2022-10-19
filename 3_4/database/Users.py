from database import BaseModel
from peewee import *


class UsersTable(BaseModel):
    user_id = PrimaryKeyField(null=False)
    name = TextField()
    telegram_id = IntegerField(unique=True)
    phone = TextField()
    email = TextField()
    address = TextField()

    @staticmethod
    def add_user(name, telegram_id):
        return UsersTable.create(name=name, telegram_id=telegram_id)

    @staticmethod
    def get_user(id):
        return UsersTable.get(user_id=id)
    
    def print_user(self):
        print(self.user_id, self.name, self.telegram_id)
    
    def set_telegram_id(self, telegram_id):
        # self.telegram_id = telegram_id
        self.update(telegram_id=telegram_id).execute()

    

