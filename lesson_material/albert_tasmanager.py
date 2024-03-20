import os, time

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import (
    PyMongoError,
    ConnectionFailure,
    ConfigurationError,
    CollectionInvalid,
    ExecutionTimeout,
    OperationFailure,
    ServerSelectionTimeoutError,
)
from typing import Dict, List, Optional, Union


class MongoCRUD:
    def __init__(
        self, host: str, port: int, database_name: str, collection_name: str
    ) -> None:
        self.host = host
        self.port = port
        self.database_name = database_name
        try:
            self.collection = self.__connect_to_mongodb()[collection_name]
        except CollectionInvalid as err:
            print(f"Collection creation error: {err}")

    def __connect_to_mongodb(self) -> Union[Database, None]:
        try:
            client = MongoClient(self.host, self.port)
            database = client[self.database_name]
            return database
        except ConnectionFailure as err:
            print(f"Connection failure: {err}")
        except ConfigurationError as err:
            print(f"Configuration error: {err}")

    def find_documents(self, query: Dict) -> Union[List[Dict], None]:
        try:
            documents = self.collection.find(query, {"_id": 0})
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def insert_one_document(self, document: Dict) -> Optional[str]:
        try:
            result = self.collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def insert_many_documents(self, document: Dict) -> Union[str, None]:
        try:
            result = self.collection.insert_many(document)
            return str(result.inserted_ids)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def update_one_document(self, query: Dict, update: Dict) -> Union[int, None]:
        try:
            result = self.collection.update_one(query, {"$set": update})
            return result.modified_count
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def update_many_documents(self, query: Dict, update: Dict) -> Union[int, None]:
        try:
            result = self.collection.update_many(query, {"$set": update})
            return result.modified_count
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def delete_one_document(self, query: Dict) -> Union[int, None]:
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def delete_many_documents(self, query: Dict) -> Union[int, None]:
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_equal(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$eq": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_greater_than(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$gt": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_greater_or_equal(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$gte": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_specified_values(
        self, key: str, values_list: list, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$in": values_list}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_less_than(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$lt": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_less_or_equal(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$lte": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_not_equal(
        self, key: str, value: int, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$ne": value}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_all_instead_of(
        self, key: str, values_list: list, parameters={}
    ) -> Union[List[Dict], None]:
        query = {key: {"$nin": values_list}}
        try:
            documents = self.collection.find(query, parameters)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")



database = MongoCRUD(
    host="localhost",
    port=27017,
    database_name="task_manager",
    collection_name="tasks",
)


def add_task() -> None:
    os.system("cls")
    task_name = input("Enter new task name: ")
    task_description = input("Enter new task description: ")
    document = {"task": task_name, "description": task_description, "status": "pending"}
    database.insert_one_document(document)
    print(f"\nTask {task_name} has been added")
    time.sleep(1.5)


def view_all_tasks() -> None:
    os.system("cls")
    all_tasks = database.find_documents({})
    counter = 1
    for task in all_tasks:
        print(
            f"\nTask {counter}: {task['task']}\nDescription: {task['description']}\nStatus: {task['status']}"
        )
        counter += 1
    input("\nPress enter to continue...")


def update_status() -> None:
    os.system("cls")
    task_name = input("Enter task you want to update name: ")
    check_task = database.find_documents({"task": task_name})
    if check_task:
        task_status = input(f"Enter new status to {task_name}: ")
        query = {"task": task_name}
        update = {"status": task_status}
        database.update_one_document(query, update)
        print(f"\nTask {task_name} status has been changed to {task_status}")
    else:
        print("There is no such task")
    time.sleep(1.5)


def delete_task() -> None:
    os.system("cls")
    task_name = input("Enter task you want to update name: ")
    check_task = database.find_documents({"task": task_name})
    if check_task:
        query = {"task": task_name}
        database.delete_one_document(query)
        print(f"\nTask {task_name} has been deleted")
    else:
        print("There is no such task")
    time.sleep(1.5)


def main_menu() -> None:
    while True:
        os.system("cls")
        print("\n------------------\n|--TASK MANAGER--|\n------------------")
        category: str = input(
            "--Menu--\n1. Add new task\n2. View all tasks\n3. Update the status of a task\n4. Delete a task\n5. Exit\n\nEnter number of selection: "
        )
        if category.isnumeric() == True:
            if category == "1":
                add_task()
            elif category == "2":
                view_all_tasks()
            elif category == "3":
                update_status()
            elif category == "4":
                delete_task()
            elif category == "5":
                print("\nBye.")
                break
            else:
                print("\nThere is no such selection")
                time.sleep(1.5)
        else:
            print(
                "\nPlease enter number from list provided without any symbols and spaces."
            )
            time.sleep(2)


main_menu()