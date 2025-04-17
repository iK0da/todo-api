from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
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
        return jsonify({"error": "Date and task are required"}), 400

    # Verifica se a data tem apenas o dia (ex: "23")
    if data["date"].isdigit() and len(data["date"]) <= 2:
        today = datetime.today()
        formatted_date = f"{data['date'].zfill(2)}/{today.month:02d}/{today.year}"
    else:
        formatted_date = data["date"]  # Usa a data como está

    new_task = {
        "date": formatted_date,
        "task": data["task"],
        "status": "pending"
    }
    tasks_collection.insert_one(new_task)
    return jsonify({"message": "Task added successfully"}), 201

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)