import datetime
from random import randint, uniform
import random
from faker import Faker
from pymongo import MongoClient
from typing import Dict, List, Optional, Union
from pymongo.errors import PyMongoError, WriteError, OperationFailure


class MongoDB:
    GMP = 0.20
    HEALT_TAX = 0.15
    TAX_FREE = 0.10

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
        start_year = datetime.datetime.now() - datetime.timedelta(days=365 * 65)
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

    def query_in_array(
        self, field_name: str, value: List, parameter: Dict = {}
    ) -> List[dict]:
        try:
            query = {field_name: {"$in": value}}
            result = self.collection.find(query, parameter).limit(10)
            return list(result)
        except OperationFailure as e:
            print("An error occurred:", str(e))
        except PyMongoError as e:
            print("Somthing has happen: ", str(e))

    def update_one_document(self, query: Dict, update: Dict) -> Optional[int]:
        try:
            result = self.collection.update_one(query, update)
            return result.modified_count
        except WriteError as e:
            print("An error occurred:", str(e))
        except PyMongoError as e:
            print("Somthing has happen: ", str(e))

    def query_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        try:
            query = {field_name: {"$eq": value}}
            result = self.collection.find(query, parameter)
            return list(result)
        except OperationFailure as e:
            print("An error occurred:", str(e))
        except PyMongoError as e:
            print("Somthing has happen: ", str(e))

    @staticmethod
    def tax_calculator(user: dict) -> tuple[float]:
        gmp_tax = user.get("salary") * MongoDB.GMP
        tax_free = (user.get("salary") - gmp_tax) * MongoDB.TAX_FREE
        health_tax = (user.get("salary") - gmp_tax - tax_free) * MongoDB.HEALT_TAX
        total_tax = gmp_tax + health_tax
        income_left = user.get("salary") - gmp_tax - health_tax
        return (round(total_tax, 2), round(income_left, 2), user.get("salary"))
