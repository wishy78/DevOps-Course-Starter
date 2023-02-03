import pytest
from todo_app import app
from dotenv import load_dotenv, find_dotenv
import mongomock
import pymongo
from os import getenv, environ
from flask_login import login_user, AnonymousUserMixin, current_user
from todo_app.data.user_class import User
from todo_app.data.mongo_items import get_currentuser

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def createfakedata():
    test_CLIENT = pymongo.MongoClient((getenv('CON_STRING')))
    test_DB = test_CLIENT[(getenv('DB_NAME'))]
    test_COLLECTION = test_DB[(getenv('COLLECTION_NAME'))]
    test_card = {"name": 'Test card', "state": "To Do"}
    test_COLLECTION.insert_one(test_card)
    test_user = get_currentuser()

def test_index_page(client):
    createfakedata()
    #response = {'login': 'test_User', 'id':1}
    #thisuser = User(response,response['login']) 
    #login_user(thisuser, remember=False, duration=None, force=True, fresh=True)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()