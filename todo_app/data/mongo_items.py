import pymongo
from os import getenv
from todo_app.data.task_class import Task
from flask_login import current_user, AnonymousUserMixin
import random 
import string
from pymongo.errors import ServerSelectionTimeoutError

def read_env_deatils():
    global CLIENT
    global DB
    global COLLECTION
    CLIENT = pymongo.MongoClient((getenv('CON_STRING')))
    DB = CLIENT[(getenv('DB_NAME'))]
    COLLECTION = DB[(getenv('COLLECTION_NAME'))]
    
def get_lists():
    return [{"id":"To Do","name":"To Do"},{"id":"Doing","name":"Doing"},{"id":"Done","name":"Done"}]

def test_connection():
    try:
        info = CLIENT.server_info() # Forces a call.
        return "Connected to Database"
    except ServerSelectionTimeoutError:
        return "Database connection is down."

def get_cards():
    cards = []
    test_connection()
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
    if ClientID.strip() in {'65459782','1'}:
        return "writer"
    # default readers
    else:
        return "disabled"

def get_currentuser():
    if not isinstance(current_user._get_current_object(), AnonymousUserMixin):
        return current_user
    else:
        current_user.login='Anonymous_User'
        current_user.id='1'
        return current_user

def randStr(chars = string.ascii_letters + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))