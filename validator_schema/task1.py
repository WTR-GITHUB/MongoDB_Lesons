from random import randint
from typing import Optional
from faker import Faker
from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError

client = MongoClient("mongodb://localhost:27017/")
db = client["exercise_db"]
collection = db["exercise_collection"]


def create_random_person() -> Optional[str]:
    fake = Faker()
    name = fake.first_name()
    age = randint(18, 99)
    email = f"{name}@{fake.last_name()}.com"

    document = {
        "name": name,
        "age": age,
        "email": email,
    }
    result = collection.insert_one(document)

    return str(result.inserted_id)


def generate_data_base(numb_of_documents):
    for _ in range(numb_of_documents):
        create_random_person()


# Define the validation rules as a dictionary
validation_rules = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "age", "email"],
            "properties": {
                "name": {"bsonType": "string"},
                "age": {"bsonType": "int", "minimum": 18, "maximum": 99},
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                },
            },
        }
    }
}

# Set the validation rules for the collection
try:
    new_collection = db.create_collection(
        name="exercise_collection",
    )
    db.command("collMod", new_collection.name, **validation_rules)
    print("Schema validation enabled.")
    generate_data_base(3)
except OperationFailure as e:
    print(f"Failed to enable schema validation: {e.details['errmsg']}")

# Clean up (optional)
client.close()


# try:
#     collection = db.create_collection(
#         collection,
#         validator=validation_rules,
#     )
#     print("Schema validation enabled for collection:")
# except PyMongoError as e:
#     print(f"Error enabling schema validation: {e}")

# data = {"name": "John", "age": 30, "email": "john@gmail.com"}
# generate_data_base(3)
