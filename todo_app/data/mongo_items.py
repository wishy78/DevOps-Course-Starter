import pymongo
from os import getenv
from todo_app.data.task_class import Task
from flask_login import current_user

def read_env_deatils():
    global CLIENT
    global DB
    global COLLECTION
    CLIENT = pymongo.MongoClient((getenv('CON_STRING')))
    DB = CLIENT[(getenv('DB_NAME'))]
    COLLECTION = DB[(getenv('COLLECTION_NAME'))]
    
def get_lists():
    return [{"id":"To Do","name":"To Do"},{"id":"Doing","name":"Doing"},{"id":"Done","name":"Done"}]

def get_cards():
    cards = []
    for card in COLLECTION.find():
        cards.append(Task.from_Mongo_card(card))
    return cards

def move_card(card, state):
    COLLECTION.update_one({"_id": (card)},{"$set": { "state": (state)}})
    return 0

def add_card(title):
    card = {"name": title, "state": "To Do"}
    COLLECTION.insert_one(card)
    return 0

def get_myrole(ClientID):
    #Authorised Writers
    if ClientID.strip() in {'65459782'}:
        return ""
    # default readers
    else:
        return "disabled"

def get_currentuser():
    return current_user