import datetime
from random import randint
from faker import Faker
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Dict, List


class MongoDB:
    def __init__(
        self, host: str, port: int, db_name: str, collection_name: str
    ) -> None:
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def find_documents(self, query: Dict) -> List[Dict]:
        documents = self.collection.find(query)
        return list(documents)

    def update_one_document(self, query: Dict, update: Dict) -> int:
        result = self.collection.update_one(query, {"$set": update})
        return result.modified_count
    
    def update_many_document(self, query: Dict, update: Dict) -> int:
        result = self.collection.update_many(query, {"$set": update})
        return result.modified_count

    def delete_one_documents(self, query: Dict) -> int:
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_many_documents(self, query: Dict) -> int:
        result = self.collection.delete_many(query)
        return result.deleted_count

    def insert_one_document(self, document: Dict) -> str:
        result = self.collection.insert_one(document)
        print(f"Printed result: {result}")
        return str(result.inserted_id)
    
    def insert_many_document(self, document: Dict) -> List[str]:
        result = self.collection.insert_many(document)
        print(f"Printed result: {result}")
        return list(result.inserted_ids)

    def create_random_person(self) -> str:
        fake = Faker()
        name = fake.first_name()
        surname = fake.last_name()
        age = randint(18, 65)
        now = datetime.datetime.now()
        years_employed = now.year - age

        document = {
            "name": name,
            "surname": surname,
            "age": age,
            "years_employed": years_employed,
        }
        result = self.collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")
        print(f"This person was inserted into the database: {document}")

        return str(result.inserted_id)

    def generate_data_base(self, numb_of_documents):
        for _ in range(numb_of_documents):
            self.create_random_person()


if __name__ == "__main__":
    mongodb = MongoDB(
        host="localhost",
        port=27017,
        db_name="persons",
        collection_name="employees_night_shift",
    )

    query = {"name": "Steven"}
    results = mongodb.find_documents(query)
    print("Matching documents:")
    for result in results:
        print(result)

    query = {"name": "Steven"}
    update = {"age": 99}
    modified_count = mongodb.update_many_document(query, update)
    print(f"Modified {modified_count} documents")

    query = {"name": "Steven"}
    deleted_count = mongodb.delete_many_documents(query)
    print(f"Deleted {deleted_count} documents")


    # numb_of_documents = 50
    # mongodb.generate_data_base(numb_of_documents)
