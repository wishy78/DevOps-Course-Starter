from requests import get,post
from flask import session
from os import getenv
from dotenv import load_dotenv

load_dotenv()

KEY = getenv('TRELLO_KEY')
TOKEN = getenv('TRELLO_TOKEN')
board = getenv('TRELLO_BOARD_ID')


def get_cards():
    lists = get_lists()
    url = f"https://api.trello.com/1/boards/{board}/cards?fields=idList,name&key={KEY}&token={TOKEN}"
    response = get(url)
   # response.status_code
   # response.text
    json_value = response.json()
    for card in json_value : 
        for list in lists:
            if card["idList"] == list["id"]:
                card["idList"] = list["name"]
    return session.get('cards', json_value)

def get_lists():
    url = f"https://api.trello.com/1/boards/{board}/lists?fields=id,name,idBoard&key={KEY}&token={TOKEN}"
    response = get(url)
    #response.status_code
    #response.text
    return response.json()  

def add_card(title):
    listId = " "
    lists = get_lists()
    for list in lists:
        if (list["name"] == "To Do"):
            listId = list["id"]
            break
    url = f"https://api.trello.com/1/cards?idList={listId}&key={KEY}&token={TOKEN}" 
    urldata = {'name': title, 'pos': 'top'}
    response = post(url,data = urldata)
    return

    