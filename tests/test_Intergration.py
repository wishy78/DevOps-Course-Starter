import os
import pytest
import requests
from todo_app import app
from dotenv import load_dotenv, find_dotenv


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


class StubResponse:
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


# Stub replacement for requests.get(url)
def stub(url, params = {}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    test_key = os.environ.get('TRELLO_KEY')
    test_token = os.environ.get('TRELLO_TOKEN')
    fake_response_data = None
   
#    url = f"https://api.trello.com/1/cards/{card}?key={KEY}&token={TOKEN}&idList={list}"
 #   url = f"https://api.trello.com/1/cards?idList={listId}&key={KEY}&token={TOKEN}"

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do'
        }]
       
        #url = f"https://api.trello.com/1/boards/{board}/lists?fields=id,name,idBoard&key={KEY}&token={TOKEN}"
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists?fields=id,name,idBoard&key={test_key}&token={test_token}':
        fake_response_data = [{
            'id': '456abc',
            'name': 'To Do',
            'idBoard': '{test_board_id}',
        }]
    print(url)
               #https://api.trello.com/1/boards/None/lists?fields=id,name,idBoard&key=None&token=None
    if url == f'https://api.trello.com/1/boards/None/lists?fields=id,name,idBoard&key=None&token=None':
        fake_response_data = [{
            'id': '456abc',
            'name': 'To Do',
            'idBoard': '{test_board_id}',
        }]
         #url = f"https://api.trello.com/1/boards/{board}/cards?fields=idList,name&key={KEY}&token={TOKEN}"
    if url == f'https://api.trello.com/1/boards/{test_board_id}/cards?fields=idList,name&key={test_key}&token={test_token}':
        fake_response_data = [{
            'cards': [{'idList': '123abc', 'name': 'Test card'}]
        }] 
    if url == f'https://api.trello.com/1/boards/None/cards?fields=idList,name&key=None&token=None':
        fake_response_data = [{
            'cards': [{'idList': '123abc', 'name': 'Test card'}]
        }]      

        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')


def test_index_page(monkeypatch, client):
    # Replace requests.get(url) with our own function
    monkeypatch.setattr(requests, 'get', stub)

    # Make a request to our app's index page
    response = client.get('/')

    assert response.status_code == 200
    assert 'Test card' in response.data.decode()

