import os
from bson import ObjectId
from flask import Flask, render_template
from modules import MongoDB
from config import HOST, PORT, DB_NAME, COLLECTION_NAME
from pymongo.errors import ConnectionFailure, PyMongoError, ConfigurationError

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"

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


@app.route("/")
def index():
    return "Hello, Flask is running!"


@app.route("/user/<user_id>")
def display_user(user_id):
    user_data = mongodb.query_equal(field_name="_id", value=ObjectId(user_id))
    return render_template("index.html", user_data=user_data[0])



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
