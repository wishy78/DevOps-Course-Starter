
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
    response = get(url)
    return response.json() 

def get_cards():
    url = f"https://api.trello.com/1/boards/{board}/cards?fields=idList,name&key={KEY}&token={TOKEN}"
    response = get(url)
    cards_json = response.json()
    lists_json = get_lists()
    items = {}
    tasks = Task
    for card in cards_json : 
        for list in lists_json:
            if card["idList"] == list["id"]:
                card["listName"] = list["name"]
                items[tasks.from_trello_card(card)] = tasks
    return session.get('cards', items)

def move_card(card,list):
    url = f"https://api.trello.com/1/cards/{card}?key={KEY}&token={TOKEN}&idList={list}"
    response = put(url)
    return

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


