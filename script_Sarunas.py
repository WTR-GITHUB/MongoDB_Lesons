from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict
from faker import Faker
import random

def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database

def insert_document(collection: Collection, document: Dict) -> str:
    result = collection.insert_one(document)
    print(f"Result: {result}")
    return str(result.inserted_id)

def create_document() -> Dict:
    fake = Faker()
    name = fake.first_name()
    surname = fake.last_name()
    age = random.randint(18, 100)
    years_emp = random.randint(0, 50)
    
    return {
        "name": name,
        "surname": surname,
        "age": age,
        "years_emp": years_emp 
    }

if __name__ == "__main__":
    mongodb_host = 'localhost'
    mongodb_port = 27017
    database_name = 'people'
    collection_name = 'employees'

    db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)
    collection = db[collection_name]

    itteration = 2
    for _ in range(itteration):
        document = create_document()
        inserted_id = insert_document(collection, document)
        print(f"Inserted document with ID: {inserted_id}")