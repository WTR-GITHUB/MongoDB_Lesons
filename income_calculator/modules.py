import datetime
from random import randint, uniform
import random
from faker import Faker
from pymongo import MongoClient
from typing import Dict, List, Optional, Union
from pymongo.errors import PyMongoError, WriteError, OperationFailure


class MongoDB:
    def __init__(
        self, host: str, port: int, db_name: str, collection_name: str
    ) -> None:
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_random_person(self) -> Optional[str]:
        fake = Faker()
        name = fake.first_name()
        surname = fake.last_name()
        start_year = datetime.datetime.now() - datetime.timedelta(days=365*65)
        end_year = datetime.datetime.now()
        random_days = random.randint(0, (end_year - start_year).days)
        random_date = start_year + datetime.timedelta(days=random_days)
        year_salary = round(uniform(15000.00, 2499.99), 2)
        age = end_year.year - random_date.year - 1

        document = {
            "name": name,
            "surname": surname,
            "birth_day": random_date,
            "age": age,
            "salary": year_salary,
        }
        result = self.collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")
        print(f"This person was inserted into the database: {document}")

        return str(result.inserted_id)

    def generate_data_base(self, numb_of_documents):
        for _ in range(numb_of_documents):
            self.create_random_person()

    def query_in_array(self, field_name: str, value:List, parameter: Dict = {}) -> List[dict]:
        try:
            query = {field_name: {"$in": value}}
            result = self.collection.find(query, parameter).limit(10)
            return list(result)
        except OperationFailure as e:
            print('An error occurred:', str(e))
        except PyMongoError as e:
            print("Somthing has happen: ", str(e))