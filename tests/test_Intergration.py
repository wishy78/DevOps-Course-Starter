import os
import pytest
import requests
from todo_app import app
from dotenv import load_dotenv, find_dotenv


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

import pymongo
from json import dumps
from os import getenv
from todo_app.data.task_class import Task

def stub(url, params = {}):
    test_CLIENT = pymongo.MongoClient((getenv('CON_STRING')))
    test_DB = test_CLIENT[(getenv('DB_NAME'))]
    test_COLLECTION = test_DB[(getenv('COLLECTION_NAME'))]
    fake_response_data = None
   #so we are testing connection to data and its reply 
   #so prehaps look to make connection again with returned fake data
    cards = []
    for card in test_COLLECTION.find():
        cards.append(Task.from_Mongo_card(card))
    if cards:
        fake_response_data = [{
            'id': '456abc',
            'name': 'To Do',
            'idBoard': 'To Do',
        }]

    if fake_response_data :
        return StubResponse(fake_response_data)
    raise Exception(f'Integration test did not expect this response "{cards}"')

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()