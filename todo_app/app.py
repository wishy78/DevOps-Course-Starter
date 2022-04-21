from flask import Flask, redirect, render_template, request
from todo_app.data.trello_items import add_card, get_cards, get_lists, move_card
from todo_app.flask_config import Config

from todo_app.data.trello_items import get_cards, add_card, get_list
app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    cards = get_cards()
    lists = get_lists()
    return render_template('index.html',cards=cards,lists=lists)
    #return render_template('index.html',cards=cards)

@app.route('/new',methods=['POST'])
def new():
    add_card(request.form.get('title') )
    #add_item(request.form.get('title') )
    return redirect('/')


@app.route('/move/<cardID>/<newList>')
def move(cardID,newList):
    move_card(cardID,newList)
    return redirect('/')

