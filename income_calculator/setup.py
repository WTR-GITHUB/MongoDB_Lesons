from app import mongodb

try:
    documents_amount = int(input("Please enter number of documents to generate in data base: "))
    mongodb.generate_data_base(documents_amount)
except ValueError as e:
    print(f"You have failed to enter integer ", e)
except TypeError as e:
    print(f"You have failed to enter integer ", e)
except Exception as e:
    print(e)