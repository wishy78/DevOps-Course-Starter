import requests
import pymongo
from os import getenv
from todo_app.data.task_class import Task

def read_env_deatils():
    global CLIENT
    global DB
    global COLLECTION
    CLIENT = pymongo.MongoClient(getenv('CON_STRING'))
    DB = CLIENT[getenv('DB_NAME')]
    COLLECTION = DB[getenv('COLLECTION_NAME')]

def get_cards():
    tasks = []
    for task in COLLECTION.find():
        tasks.append(Task.from_Mongo_card(task))
    return tasks

def move_card(task, state):
    COLLECTION.update({"_id": task._id},{set: { "state": state}})
    return 0

def add_card(title):
    task = {"name": title, "state": "To-Do"}
    COLLECTION.insert_one(task)
    return 0
