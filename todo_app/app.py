from flask import Flask, redirect, render_template, request
from todo_app.data.trello_items import add_card, get_cards
from todo_app.flask_config import Config



app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    cards = get_cards()
    return render_template('index.html',cards=cards)

@app.route('/new',methods=['POST'])
def new():
    add_card(request.form.get('title') )
    #add_item(request.form.get('title') )
    return redirect('/')




