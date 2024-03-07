from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import List


def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


def get_database_collection(database: Database, collection_name: str) -> Collection:
    collection = database[collection_name]
    return collection


def list_databases(client: MongoClient) -> List[str]:
    return client.list_database_names()


def list_collections(database: Database) -> List[str]:
    return database.list_collection_names()


# Example usage
if __name__ == "__main__":
    # Connection details
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "mydatabase"
    collection_name = "mycollection"

    # # Connect to MongoDB
    client = MongoClient(mongodb_host, mongodb_port)
    # db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)

    # # Retrieve a specific collection
    # collection = get_database_collection(db, collection_name)
    # print(f"Retrieved collection: {collection_name}")

    # List all databases
    databases = list_databases(client)
    print("List of databases:")
    print(f"Data base type: {type(databases)}, {databases}")

    for db_name in databases:
        print(db_name)

    # List collections in the connected database
    # collections = list_collections(db)
    # print("Collections in the connected database:")
    # for collection_name in collections:
    #     print(collection_name)
