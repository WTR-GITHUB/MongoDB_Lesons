# Create a CLI application that takes name surname gender and age (in a single sentence).
# Check if gender or age is provided correctly. Result save to database with timestamp of the event.

import datetime
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


data_input = input("Please enter name, gender(male, female) and age: ")


try:
    
    data_list = data_input.split(" ")

    if len(data_list) >= 3:
        if data_list[1] == "male" or data_list[1] == "female":
            gender = data_list[1]

        if data_list[2].isdigit():
            age = int(data_list[2])

        name = data_list[0]

        now = datetime.datetime.now()

    else:
        print("Input data is not formatted correctly.")

except Exception as error:
    print(error)



if __name__ == "__main__":
    # Connection details
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "task1"
    collection_name = "task1_colection"

    try:
        # Connect to MongoDB
        db = connect_to_mongodb(host=mongodb_host, port=mongodb_port, db_name=database_name)

        # Retrieve a specific collection
        collection = db[collection_name]

        # Create (Insert) Operation
        document = {
            "name": name,
            "gender": gender,
            "age": age,
            "lastModified": now,
        }
        inserted_id = insert_document(collection=collection, document=document)
        print(f"Inserted document with ID: {inserted_id}")
    except Exception as error:
        print(f"Error input data: {error}")
