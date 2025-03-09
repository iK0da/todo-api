from flask import Flask
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["todo_list"]

@app.route("/")
def home():
    return {"message": "Todo List API"}

if __name__ == "__main__":
    app.run(debug=True)