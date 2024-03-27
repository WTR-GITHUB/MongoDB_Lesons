import os
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
    print("Connection failure:", str(e))
except ConfigurationError as e:
    print("Configuration failure:", str(e))
except PyMongoError as e:
    print("General failure:", str(e))

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
@click.option(
    "--start",
    default=18,
    prompt="Please enter start age range",
    help="Start of age range",
    type=int,
)
@click.option(
    "--end",
    default=65,
    prompt="Please enter end age range",
    help="End of age range",
    type=int,
)
@click.option(
    "--all", "all_info", is_flag=True, help="Print all information about persons."
)
def get_persons(start, end, all_info) -> dict:
    os.system("cls||clear")
    result = mongodb.query_in_array(field_name="age", value=[start, end])
    count = 0
    menu_map = {}
    print(
        f"{'ID':<2s} : {'Name':<15s}\t{'Surname':<10s}\t{'Birth day':<20s}\t{'Age':<5s}"
    )
    print("------------------------------------------------------------------------")
    for res in result:
        count += 1
        if all_info:
            print(
                f"{count:2d} : {res['name']:15s}\t{res['surname']:10s}\t{res['birth_day'].strftime('%Y-%m-%d'):10s}\t{res['age']:10d}"
            )
        else:
            print(f"{count:2d} : {res['name']:10s}")

        menu_map[count] = res["_id"]
    user_choice = input("\nPlease enter user's number: ")
    selected_user = menu_map.get(int(user_choice))
    user = mongodb.query_equal(field_name="_id", value=selected_user)
    tax = mongodb.tax_calculator(user=user[0])

    # update = {}
    # user = mongodb.update_one_document(query={"_id":selected_user})
    print(tax)


if __name__ == "__main__":
    get_persons()
