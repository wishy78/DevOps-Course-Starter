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

def stub(url, params = {}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    test_key = os.environ.get('TRELLO_KEY')
    test_token = os.environ.get('TRELLO_TOKEN')
    fake_response_data = None
   
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists?fields=id,name,idBoard&key={test_key}&token={test_token}':
        fake_response_data = [{
            'id': '456abc',
            'name': 'To Do',
            'idBoard': '{test_board_id}',
        }]

    if url == f'https://api.trello.com/1/boards/{test_board_id}/cards?fields=idList,name&key={test_key}&token={test_token}':
        fake_response_data = [{
            'idList': '456abc', 'name': 'Test card', 'id' : '789abc'
        }] 

    if fake_response_data :
        return StubResponse(fake_response_data)
    raise Exception(f'Integration test did not expect URL "{url}"')

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()