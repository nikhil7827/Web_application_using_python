from flask import Flask, request, jsonify
from bson import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.todos
collection = db.todo

@app.route("/todos", methods=["GET"])
def get_all():
    todos = list(collection.find())
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def create():
    data = request.json
    todo_id = collection.insert_one(data).inserted_id
    return jsonify({"id": str(todo_id)}), 201

@app.route("/todos/<id>", methods=["GET"])
def get_one(id):
    todo = collection.find_one({"_id": ObjectId(id)})
    if todo:
        todo["_id"] = str(todo["_id"])
        return jsonify(todo)
    return {"error": "Not found"}, 404

@app.route("/todos/<id>", methods=["PUT"])
def update(id):
    data = request.json
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count:
        return {"msg": "Updated"}
    return {"msg": "Nothing updated"}, 200

@app.route("/todos/<id>", methods=["DELETE"])
def delete(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"msg": "Deleted"}
    return {"msg": "Nothing deleted"}, 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
