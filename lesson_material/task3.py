# Create a python script that would generate a sequence of 1000 random numbers from 1 to 1000000 .
# A number sequence from 0 to 9 represents letters from A to J.
# (lets say we have 101 = BAB) . All those 1000 values should be written to database (number and it's representation) 
# Please find: 
# - All documents where number is 100,1000,10000
# - All documents where numbers are at least triple or four digits
# - What is the dominant letter within  five and 6 digits area range. 
# - Tell me the sum on numbers where majority letters are : (letter 1, letter 2, letter 3)
# - Show me the lowest and highest number and their representations

from collections import Counter
from random import randint
from pymongo import MongoClient
from typing import Dict, List
import string

class MongoDB:
    def __init__(
        self, host: str, port: int, db_name: str, collection_name: str
    ) -> None:
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def find_documents(self, query: Dict) -> List[Dict]:
        documents = self.collection.find(query)
        return list(documents)


    def convert_numb_to_letters(self, numbers):
        number_list = [int(numb) for numb in str(numbers)]
        print(number_list)
        alpha_dict = dict(enumerate(string.ascii_lowercase))
        print(alpha_dict)
        return "".join([alpha_dict[x] for x in number_list])

    def random_data(self) -> str:
        random_numb = randint(1, 1000000)

        document = {
            "number":random_numb,
            "number_map": self.convert_numb_to_letters(random_numb),
        }
        result = self.collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")
        print(f"This person was inserted into the database: {document}")

        return str(result.inserted_id)

    def generate_data_base(self, numb_of_documents):
        for _ in range(numb_of_documents):
            self.random_data()


if __name__ == "__main__":
    mongodb = MongoDB(
        host="localhost",
        port=27017,
        db_name="numbers",
        collection_name="maping_numbers",
    )

# - All documents where number is 100,1000,10000
    query_1 = {"number": 100, "number": 1000, "number": 10000}
    results = mongodb.find_documents(query_1)
    print("Matching documents Query 1:")
    for result in results:
        print(result)

# - All documents where numbers are at least triple or four digits
    query_2 = {"number": {"$gt":100, "$lt":10000}}
    results = mongodb.find_documents(query_2)
    print("Matching documents Query 2:")
    for result in results:
        print(result)

# - What is the dominant letter within five and 6 digits area range. 
    query_3 = {"number": {"$gt":10000, "$lt":1000000}}
    results = mongodb.collection.find(query_3, {"_id":0,"number_map":1})
    
    for result in results:
        count = Counter(result["number_map"])
        sorted_data = dict(sorted(count.items(), key=lambda item: item[1], reverse=True))
        max_key = max(sorted_data, key=sorted_data.get)
        if sorted_data[max_key] > 1:
            print(f"Matching documents Query 3: {result}, {max_key} = {sorted_data[max_key]}")

# - Tell me the sum on numbers where majority letters are : (letter 1, letter 2, letter 3)
    query_4 = {"number": {"$gt":10000, "$lt":1000000}}
    results = mongodb.collection.find(query_4, {"_id":0})
    
    a_list = []
    b_list = []
    c_list = []
    for result in results:
        count = Counter(result["number_map"])
        sorted_data = dict(sorted(count.items(), key=lambda item: item[1], reverse=True))
        max_key = max(sorted_data, key=sorted_data.get)
        if sorted_data[max_key] > 1 and max_key == "a":
            a_list.append(result["number"])
        elif sorted_data[max_key] > 1 and max_key == "e":
            b_list.append(result["number"])
        elif sorted_data[max_key] > 1 and max_key == "f":
            c_list.append(result["number"])
    print(f"Matching documents Query 4 letter 'a': {sum(a_list)}")
    print(f"Matching documents Query 4 letter 'e': {sum(b_list)}")
    print(f"Matching documents Query 4 letter 'f': {sum(c_list)}")
    print(f"Max number: {max(a_list)}")
    print(f"Max number: {max(b_list)}")
    print(f"Max number: {max(c_list)}")

    query_10 = {"number": max(a_list)}
    results = mongodb.collection.find(query_10)
    print("Matching documents Query 10:")
    for result in results:
        print(result)