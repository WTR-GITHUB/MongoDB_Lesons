from pymongo import MongoClient
from pymongo.errors import OperationFailure

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["task1"]
collection = db["task1_colection"]

# Define the validation rules as a dictionary
validation_rules = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "age", "email"],
            "properties": {
                "name": {"bsonType": "string"},
                "age": {"bsonType": "int", "minimum": 0},
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
    # db.command('collMod', collection.name, **validation_rules)
    # print("Schema validation enabled.")
    document = {
        "name": "Saulius",
        "age": 20,
        "email": "saulius@gmail.com",
        "surname": "Anusas",
    }
    result = collection.insert_one(document)
except OperationFailure as e:
    print(f"Failed to enable schema validation: {e.details['errmsg']}")

# Clean up (optional)
client.close()


schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "age", "email"],
            "properties": {
                "name": {"bsonType": "string"},
                "age": {"bsonType": "int", "minimum": 18},
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                },
            },
        }
    }

    # Enable schema validation for the collection
try:
    collection = db.create_collection(
        collection_name,
        validator=schema,
    )
    print("Schema validation enabled for collection:")
except PyMongoError as e:
    print(f"Error enabling schema validation: {e}")

data = {"name": "John", "age": 30, "email": "john@gmail.com"}
collection.insert_one(data)
