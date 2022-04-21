from flask import Flask, redirect, render_template, request
from todo_app.data.trello_items import add_card, get_cards, get_lists, move_card
from todo_app.flask_config import Config
from  todo_app.data.task_class import task,from_trello_card


app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    #tt = task()
    # so a class to hold a record
    # so do i need multiple class items in a dictionary?
    # where using a class to default settings so other systems can be used with minimal change
    # eg task(ID, Name, State) (but this is in trello ID Name IDlist(name))
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

