import os
from mongo_modules import MongoDB
from manager_setup import HOST, PORT, DB_NAME, COLLECTION_NAME
from datetime import datetime, timedelta
from task_modules import Task
from pymongo.errors import ConnectionFailure, PyMongoError, ConfigurationError

if __name__ == "__main__":
    try:
        mongodb = MongoDB(
            host=HOST,
            port=int(PORT),
            db_name=DB_NAME,
            collection_name=COLLECTION_NAME,
        )
    except ConnectionFailure as e:
        print('Connection failure:', str(e))
    except ConfigurationError as e:
        print('Configuration failure:', str(e))
    except PyMongoError as e:
        print('General failure:', str(e))

    def input_task_details() -> Task:
        name = input("Enter the task name: ")
        status = input("Enter the task status (Not started/In progress/Completed): ")
        due_to_input = input("Enter the due date for the task (format YYYY-MM-DD), or leave blank for default (7 days from now): ")
        due_to = datetime.strptime(due_to_input, "%Y-%m-%d") if due_to_input else datetime.now() + timedelta(days=7)
        task = Task(name=name, status=status, due_to=due_to)
        return task


    result = mongodb.get_all_documents()
    for res in result:
        print(f"Task name: {res['name']}, status: {res['status']}")
        print(f"Task due to: {res['due_to']}")
