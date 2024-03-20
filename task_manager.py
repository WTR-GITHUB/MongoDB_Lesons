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
        status_input = input("Enter the task status (Not started/In progress/Completed), or leave blank for default: ")
        accepted_statuses = ["Not started", "In progress", "Completed"]
        status = status_input if status_input in accepted_statuses else "Not started"
        due_to_input = input("Enter the due date for the task (format YYYY-MM-DD), or leave blank for default (7 days from now): ")
        due_to = datetime.strptime(due_to_input, "%Y-%m-%d") if due_to_input else datetime.now() + timedelta(days=7)
        task = Task(name=name, status=status, due_to=due_to)
        return task
    
    def print_all_tasks() -> None:
        result = mongodb.get_all_documents()
        if result:
            for res in result:
                print(f"Task name: {res['name']}, status: {res['status']}")
                print(f"Task due to: {res['due_to']}")
        else:
            print("No tasks found or an error occurred.")

    def print_main_menu() -> None:
        print("""
Welcome to the task manager please chose command by entering number in commend line:
1. Add a new task.
2. View all tasks.
3. Close the program.
""")
    def print_second_menu() -> None:
        print("""Please chose command:
1. Delete task
2. Update task status
b. Go back to main menu.
""")
    
    os.system('cls||clear')
    print_main_menu()

    user_input = input()

    while True:
        try:
            if user_input =="1":
                os.system('cls||clear')
                task = input_task_details()
                new_task = task.create_task()
                inserted = mongodb.insert_one_document(document=new_task)
                if inserted is not None:
                    print(f"Task created.")
                else:
                    print("Failed to create task.")
                print_main_menu()
                user_input = input()

            elif user_input =="2":
                os.system('cls||clear')
                print_all_tasks()
                print("\n===========================================\n")
                print_second_menu()
                while user_input != "b":
                    user_input = input().lower()
                    try:
                        if user_input =="1":
                            os.system('cls||clear')
                            print_all_tasks()
                            print("\n===========================================\n")
                            task_name = input("Please enter task name to delete: ")
                            result = mongodb.query_equal(field_name="name", value=task_name)
                            query = {"name": task_name}
                            delete = mongodb.delete_one_documents(query=query)
                            if delete > 0:
                                os.system('cls||clear')
                                print(f"Task '{task_name}' deleted successfully.\n")
                                print_all_tasks()
                                print("\n===========================================\n")
                                print_second_menu()
                            else:
                                os.system('cls||clear')
                                print_all_tasks()
                                print("\n===========================================\n")
                                print(f"Task '{task_name}' not found.")
                                print("\n===========================================\n")
                                print_second_menu()
                        elif user_input =="2":
                            os.system('cls||clear')
                            print_all_tasks()
                            print("\n===========================================\n")
                            task_name = input("Please enter task name to update status: ")
                            tasks_to_update = mongodb.query_equal(field_name="name", value=task_name)

                            os.system('cls||clear')
                            if tasks_to_update:
                                print("Please choose status:")
                                print("1. Not started")
                                print("2. In progress")
                                print("3. Completed")
                                status_choice = input()

                                status_map = {
                                    "1": "Not started",
                                    "2": "In progress",
                                    "3": "Completed"
                                }
                                new_status = status_map.get(status_choice)
                                if new_status:
                                    update = {"$set": {"status": new_status}}
                                    update_result = mongodb.update_one_document(query={"name": task_name}, update=update)
                                    if update_result > 0:
                                        os.system('cls||clear')
                                        print(f"Task '{task_name}' status updated to '{new_status}'.")
                                        print_all_tasks()
                                        print("\n===========================================\n")
                                        print_second_menu()
                                    else:
                                        os.system('cls||clear')
                                        print_all_tasks()
                                        print("\n===========================================\n")
                                        print(f"No updates made to task '{task_name}'.")
                                        print("\n===========================================\n")
                                        print_second_menu()     
                            else:
                                os.system('cls||clear')
                                print_all_tasks()
                                print("\n===========================================\n")
                                print(f"Task '{task_name}' not found.")
                                print("\n===========================================\n")
                                print_second_menu()                    
                        elif user_input == "b":
                            os.system('cls||clear')
                            print_main_menu()
                        else:
                            print("Invalid input, please try again or type 'b' to return to the main menu.")    
                    except PyMongoError as e:
                        print(f"An error occurred with MongoDB: {e}")
                    except ValueError as e:
                        print(f"An error occurred with input format: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")

            elif user_input == "3":
                os.system('cls||clear')
                print("Program closed.")
                break

            else:
                os.system('cls||clear')
                print_main_menu()
                user_input = input("Invalid input, please try again.\n")

        except PyMongoError as e:
            print(f"An error occurred with MongoDB: {e}")
        except ValueError as e:
            print(f"An error occurred with input format: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
