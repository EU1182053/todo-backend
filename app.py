from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Access environment variables

app = Flask(__name__)
# # Access environment variables
mongo_uri = os.getenv('MONGO_URI')
#
# # Use the variables in your app configuration or elsewhere
app.config['MONGO_URI'] = mongo_uri

CORS(app)
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def get_todos():
    todos = mongo.db.todos.find()
    output = []
    for todo in todos:
        output.append({'id': str(todo['_id']), 'title': todo['title'], 'completed': todo['completed']})
    return jsonify({'todos': output})


@app.route('/sorted', methods=['GET'])
def get_todos_sorted():
    todos = mongo.db.todos.find().sort("title", 1)
    output = []
    for todo in todos:
        output.append({'id': str(todo['_id']), 'title': todo['title'], 'completed': todo['completed']})
    return jsonify({'todos': output})


@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.json['title']
    completed = request.json['completed']
    todo_id = mongo.db.todos.insert_one({'title': title, 'completed': completed}).inserted_id
    new_todo = mongo.db.todos.find_one({'_id': todo_id})
    output = {'id': str(new_todo['_id']), 'title': new_todo['title'], 'completed': new_todo['completed']}
    return jsonify({'todo': output}), 201


@app.route('/todos/<string:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    title = request.json['title']
    completed = request.json['completed']
    mongo.db.todos.update_one({'_id': ObjectId(todo_id)}, {'$set': {'title': title, 'completed': completed}})
    updated_todo = mongo.db.todos.find_one({'_id': ObjectId(todo_id)})
    output = {'id': str(updated_todo['_id']), 'title': updated_todo['title'], 'completed': updated_todo['completed']}
    return jsonify({'todo': output})


@app.route('/todos/<string:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    mongo.db.todos.delete_one({'_id': ObjectId(todo_id)})
    return jsonify({'message': 'Todo deleted'})


if __name__ == '__main__':
    app.run(debug=True)
