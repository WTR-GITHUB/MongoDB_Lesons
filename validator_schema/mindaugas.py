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