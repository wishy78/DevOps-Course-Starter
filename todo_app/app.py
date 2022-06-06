from flask import Flask, redirect, render_template, request
from todo_app.data.trello_items import add_card, get_cards, get_lists, move_card, read_env_deatils
from todo_app.flask_config import Config
from todo_app.View_Class import ViewModel


def create_app():
    read_env_deatils()
    app = Flask(__name__)
    # We specify the full path and remove the import for this config so it loads the env variables when the app is created,
    # rather than when this file is imported
    app.config.from_object(Config())
    # All the routes and setup code etc
    # e.g.
    # @app.route('/')
    # def index():
    # ...
    @app.route('/')
    def index():
        item_view_model = ViewModel(get_cards())
        wwww = ViewModel(get_cards)
        print(item_view_model.doing_items)
        for item in item_view_model.doing_items:
            for i in item:
                print(i.name)
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

