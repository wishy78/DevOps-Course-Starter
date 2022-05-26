from flask import Flask, redirect, render_template, request
from todo_app.data.trello_items import add_card, get_cards, get_lists, move_card
from todo_app.flask_config import Config
from todo_app.View_Class import ViewModel

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    item_view_model = ViewModel(get_cards())
    print(item_view_model.doing_items)
    for item in item_view_model.doing_items:
        for i in item:
            print(i.name)
    #item_view_model = get_cards()
    #for item in item_view_model:
     #   print(item.name)
    return render_template('index.html', view_model=item_view_model,lists=get_lists())
    #return render_template('index.html',cards=get_cards(),lists=get_lists())
 
@app.route('/new',methods=['POST'])
def new():
    add_card(request.form.get('title') )
    return redirect('/')

@app.route('/move/<cardID>/<newList>')
def move(cardID,newList):
    move_card(cardID,newList)
    return redirect('/')