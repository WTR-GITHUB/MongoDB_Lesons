import os
from modules import MongoDB
from config import HOST, PORT, DB_NAME, COLLECTION_NAME
from pymongo.errors import ConnectionFailure, PyMongoError, ConfigurationError
import click
from flask_module import app

#============== Šito pats nesugalvojau nusižiūrėjau iš kitų, bet veikia smagu
def validate_age(ctx, param, value):
    try:
        age = int(value)
        if age < 1 or age > 65:
            raise ValueError("Age must be between 1 and 65.")
        return age
    except ValueError:
        raise click.BadParameter("Age must be an integer between 1 and 65.")
# ==========================================================================
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


@click.command()
@click.option(
    "--start",
    default=1,
    prompt="Please enter start age range",
    help="Start of age range",
    type=int,
    callback=validate_age
)
@click.option(
    "--end",
    default=65,
    prompt="Please enter end age range",
    help="End of age range",
    type=int,
    callback=validate_age
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
    while True:
        try:
            user_choice = int(input("\nPlease enter user's number: "))
            if user_choice in menu_map:
                selected_user = menu_map.get(user_choice)
                break
            else:
                print("Please chose existing ID")
        except ValueError:
            print("Stop acting like a monkey in airplane type a number")

    user = mongodb.query_equal(field_name="_id", value=selected_user)
    tax = mongodb.tax_calculator(user=user[0])

    update = {
        "$set": {
            "gmp_tax": tax[0],
            "tax_free": tax[1],
            "health_tax": tax[2],
            "total_tax": tax[3],
            "income_left": tax[4],
        }
    }
    mongodb.update_one_document(query={"_id": selected_user}, update=update)
    updated_user = mongodb.query_equal(field_name="_id", value=selected_user)
    if updated_user:
        user_url = f"http://localhost:5000/user/{updated_user[0].get('_id')}"
        print(user_url)
    else:
        print("Failed to update user.")


if __name__ == "__main__":
    get_persons()
