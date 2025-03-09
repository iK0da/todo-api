from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["todo_list"]
tasks_collection = db["tasks"]

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json

    if "date" not in data or "task" not in data:
        return jsonify({"error": "Date and task are required."}), 400
    
    new_task = {
        "date": data["date"],
        "task": data["task"],
        "status": "pending"
    }
    tasks_collection.insert_one(new_task)
    return jsonify({"message": "Task added sucessfully"}), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = list(tasks_collection.find({},{"_id":0}))
    return jsonify(tasks)

@app.route("/tasks/<task_name>", methods=["PUT"])
def update_task(task_name):
    tasks_collection.update_one(
        {"task": task_name},
        {"$set": {"status": "completed"}}
    )
    return jsonify({"message": "Task updated sucessfully"})

@app.route("/tasks/<task_name>", methods=["DELETE"])
def delete_task(task_name):
    tasks_collection.delete_one({"task": task_name})
    return jsonify({"message": "Task deleted sucessfully"})

@app.route("/")
def home():
    return {"message": "Todo List API"}

if __name__ == "__main__":
    app.run(debug=True)