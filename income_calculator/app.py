from modules import MongoDB
from config import HOST, PORT, DB_NAME, COLLECTION_NAME
from pymongo.errors import ConnectionFailure, PyMongoError, ConfigurationError
import click

# if __name__ == "__main__":
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

# =============== VEIKIANTIS ============================
# start = int(input("Please enter start age range: "))
# end = int(input("Please enter end age range: "))

# result = mongodb.query_in_array(field_name="age", value=[start, end])
# for res in result:
#     print(f"{res['name']:10s}\t{res['surname']:10s}\t{res['birth_day'].strftime('%Y-%m-%d'):10s}{res['age']:10d}")
# =============== VEIKIANTIS ============================

# def get_persons():
#     start = int(input("Please enter start age range: "))
#     end = int(input("Please enter end age range: "))
#     result = mongodb.query_in_array(field_name="age", value=[start, end])
#     for res in result:
#         print(f"{res['name']:10s}\t{res['surname']:10s}\t{res['birth_day'].strftime('%Y-%m-%d'):10s}{res['age']:10d}")


@click.command()
@click.option('--start', default=18, prompt='Please enter start age range', help='Start of age range', type=int)
@click.option('--end', default=65, prompt='Please enter end age range', help='End of age range', type=int)
@click.option('--all', 'all_info', is_flag=True, help='Print all information about persons.')
def get_persons(start, end, all_info):
    result = mongodb.query_in_array(field_name="age", value=[start, end])
    for res in result:
        if all_info:
            print(f"{res['name']:10s}\t{res['surname']:10s}\t{res['birth_day'].strftime('%Y-%m-%d'):10s}\t{res['age']:10d}")
        else:
            print(f"{res['name']:10s}")

if __name__ == '__main__':
    get_persons()