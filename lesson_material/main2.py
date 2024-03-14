from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict


def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


def insert_document(collection: Collection, document: Dict) -> str:
    result = collection.insert_one(document)
    print(f"Printed result: {result}")
    return str(result.inserted_id)


# Example usage
if __name__ == "__main__":
    # Connection details
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "leson1"
    collection_name = "leson1_colection"

    # Connect to MongoDB
    db = connect_to_mongodb(host=mongodb_host, port=mongodb_port, db_name=database_name)

    # Retrieve a specific collection
    collection = db[collection_name]

    # Create (Insert) Operation
    document = {
        "name": "Vardenis",
        "age": 30,
        "email": "johndoe@example.com",
        "title": "Mrs",
    }
    inserted_id = insert_document(collection=collection, document=document)
    print(f"Inserted document with ID: {inserted_id}")
