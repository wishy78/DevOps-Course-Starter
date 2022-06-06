import requests
from os import getenv
from todo_app.data.task_class import Task

def read_env_deatils():
    global KEY
    global TOKEN
    global board
    KEY = getenv('TRELLO_KEY')
    TOKEN = getenv('TRELLO_TOKEN')
    board = getenv('TRELLO_BOARD_ID')


def get_lists():
    url = f"https://api.trello.com/1/boards/{board}/lists?fields=id,name,idBoard&key={KEY}&token={TOKEN}"
    return requests.get(url).json()


def get_cards():
    items = []
    url = f"https://api.trello.com/1/boards/{board}/cards?fields=idList,name&key={KEY}&token={TOKEN}"
    for card in requests.get(url).json():
        for list in get_lists():
            if card["idList"] == list["id"]:
                card["listName"] = list["name"]
                items.append(Task.from_trello_card(card))
    return items


def move_card(card, list):
    url = f"https://api.trello.com/1/cards/{card}?key={KEY}&token={TOKEN}&idList={list}"
    return requests.put(url)


def add_card(title):
    listId = " "
    for list in get_lists():
        if list["name"] == "To Do":
            listId = list["id"]
            break
    url = f"https://api.trello.com/1/cards?idList={listId}&key={KEY}&token={TOKEN}"
    urlbody = {'name': title, 'pos': 'top'}
    return requests.post(url, data=urlbody)
