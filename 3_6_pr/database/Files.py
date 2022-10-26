import os
import re

from database import BaseModel, PizzaTable
from peewee import *


class FileTable(BaseModel):
    file_id = PrimaryKeyField(null=False)
    telegram_file_id = TextField()
    file_name = TextField(unique=True)

    # Add entry in pizza based on info in data for each pizza
    @staticmethod
    def check_files():
        path = "data/pizza/"
        for filename in os.listdir(path):
            print(filename)
            # Check if entry exist in DB
            list_digs = re.findall(r'\d+', filename)
            res = list(map(int, list_digs))
            exist = PizzaTable.get_or_none(pizza_id=res[0])
            if exist is None:
                # Add new entry
                if re.fullmatch(".*.txt", filename):
                    f = open(f"{path}{filename}", "r")
                    p_data = [line.strip() for line in f]
                    f.close()
                    PizzaTable.create(
                        pizza_id=res[0],
                        name=p_data[0],
                        type=p_data[1],
                        desc=p_data[2],
                        price=int(p_data[3]),
                    )

    @staticmethod
    def get_file_id_by_file_name(name):
        file: FileTable = FileTable.get_or_none(file_name=name)
        if file is None:
            return None
        return file.telegram_file_id
