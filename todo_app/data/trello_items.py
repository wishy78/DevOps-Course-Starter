
from requests import get,post,put
from flask import session
from os import getenv
from dotenv import load_dotenv
from todo_app.data.task_class import Task

load_dotenv()

KEY = getenv('TRELLO_KEY')
TOKEN = getenv('TRELLO_TOKEN')
board = getenv('TRELLO_BOARD_ID')

def get_lists():
    url = f"https://api.trello.com/1/boards/{board}/lists?fields=id,name,idBoard&key={KEY}&token={TOKEN}"
    return get(url).json() 

def get_cards():
    items = {}
    tasks = Task
    url = f"https://api.trello.com/1/boards/{board}/cards?fields=idList,name&key={KEY}&token={TOKEN}"
    for card in get(url).json(): 
        for list in get_lists():
            if card["idList"] == list["id"]:
                card["listName"] = list["name"]
                items[tasks.from_trello_card(card)] = tasks
    return session.get('cards', items)

def move_card(card,list):
    url = f"https://api.trello.com/1/cards/{card}?key={KEY}&token={TOKEN}&idList={list}"
    return put(url)

def add_card(title):
    listId = " "
    for list in get_lists():
        if (list["name"] == "To Do"):
            listId = list["id"]
            break
    url = f"https://api.trello.com/1/cards?idList={listId}&key={KEY}&token={TOKEN}" 
    urldata = {'name': title, 'pos': 'top'}
    return post(url,data = urldata)


