# Create a python script that would generate a sequence of 1000 random numbers from 1 to 1000000 . A number sequence from 0 to 9 represents letters from A to J.
# (lets say we have 101 = BAB) . All those 1000 values should be written to database (number and it's representation)
# Please find:
# - All documents where number is 100,1000,10000
# - All documents where numbers are at least triple or four digits
# - What is the dominant letter within  five and 6 digits area range.
# - Tell me the sum on numbers where majority letters are : (letter 1, letter 2, letter 3)
# - Show me the lowest and highest number and their representations

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict
import random


def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


def insert_document(collection: Collection, document: Dict) -> str:
    result = collection.insert_one(document)
    return str(result.inserted_id)


alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def create_document(alphabet) -> Dict:
    number = random.randint(1, 1000000)
    num_str = str(number)
    letters = "".join(alphabet[int(x)] for x in num_str)

    return {"number": number, "letters": letters}


# print(create_document(alphabet))

if __name__ == "__main__":
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "mongo2_task1"
    collection_name = "numbers_letters"

    db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)

    collection = db[collection_name]

    ##### CREATE DATABASE #####
    # for _ in range(1000):
    #     document = create_document(alphabet)
    #     inserted_id = insert_document(collection, document)
    #     print(f"Pair added: {document['number']} {document['letters']}")

    ##### QUERIES #####

    # 1.- All documents where number is 100,1000,10000

    # query = {"number": {"$in": [533409, 150042, 977361]}}
    # response = collection.find(query, {"_id": 0})
    # for i in response:
    #     print(i)

    # 2.- All documents where numbers are at least triple or four digits

    # query = {"number": {"$gt": 99, "$lt": 10000}}
    # response = collection.find(query, {"_id": 0})
    # for i in response:
    #     print(i)

    # 3.- What is the dominant letter within  five and 6 digits area range.

    # query = {"number": {"$gt": 9999, "$lt": 1000000}}
    # response = collection.find(query, {"_id": 0})
    # all_letters = "".join(x["letters"] for x in response)
    # dominant_letter = []

    # for letter in alphabet:
    #     count = len([1 for x in all_letters if x == letter])
    #     dominant_letter.append((letter, count))
    # max_tuple = max(dominant_letter, key=lambda x: x[1])
    # print(max_tuple)

    # 4.- Tell me the sum on numbers where majority letters are : (letter 1, letter 2, letter 3)

    # response = collection.find({}, {"_id": 0})
    # desired_letter = "C"
    # desired_letter_sum = 0
    # for i in response:
    #     letters_list = [x for x in i["letters"]]
    #     unique_letters_set = sorted(set(letters_list))
    #     letters_frequency_dict = {}
    #     for item in unique_letters_set:
    #         letters_frequency_dict[item] = letters_list.count(item)
    #     if letters_frequency_dict.get(desired_letter) == max(letters_frequency_dict.values()):
    #         desired_letter_sum += i["number"]
    # print(desired_letter_sum)

    # 5.- Show me the lowest and highest number and their representations

    response = collection.find({}, {"_id": 0})
    min_value = min(response, key=lambda x: x["number"])
    print(f"Lowest number: {min_value}")

    response = collection.find({}, {"_id": 0})
    max_value = max(response, key=lambda x: x["number"])
    print(f"Highest number: {max_value}")