import os
from mongo_modules import MongoDB
from manager_setup import HOST, PORT, DB_NAME, COLLECTION_NAME
from datetime import datetime, timedelta
from task_modules import Task



if __name__ == "__main__":
    mongodb = MongoDB(
        host=HOST,
        port=int(PORT),
        db_name=DB_NAME,
        collection_name=COLLECTION_NAME,
    )

    def input_task_details() -> Task:
        name = input("Enter the task name: ")
        status = input("Enter the task status (Not started/In progress/Completed): ")
        due_to_input = input("Enter the due date for the task (format YYYY-MM-DD), or leave blank for default (7 days from now): ")
        due_to = datetime.strptime(due_to_input, "%Y-%m-%d") if due_to_input else datetime.now() + timedelta(days=7)
        task = Task(name=name, status=status, due_to=due_to)
        return task

    os.system('cls||clear')

    print(
        """
    Welcome to the task manager please chose command by entering number in commend line:

    1. Add a new task.
    2. View all tasks.
    3. Close the program.
    """
    )

    user_input = input()

    while True:
        
        if user_input =="1":
            task = input_task_details()
            new_task = task.create_task()
            mongodb.insert_one_document(document=new_task)
            print("Task created:")
            print(new_task)
            pass
        elif user_input == "3":
            print("Closing the program.")
            break