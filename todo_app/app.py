from flask import Flask, redirect, render_template, request
from todo_app.data.mongo_items2 import add_card, get_cards, get_lists, move_card, read_env_deatils
from todo_app.flask_config import Config
from todo_app.View_Class import ViewModel


def create_app():
    read_env_deatils()
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        item_view_model = ViewModel(get_cards())
        return render_template('index.html', view_model=item_view_model, lists=get_lists())


    @app.route('/new', methods=['POST'])
    def new():
        add_card(request.form.get('title'))
        return redirect('/')


    @app.route('/move/<cardID>/<newList>')
    def move(cardID, newList):
        move_card(cardID, newList)
        return redirect('/')

    return app

