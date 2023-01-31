from flask import Flask, redirect, render_template, request
from todo_app.data.trello_items import add_card, get_cards, get_lists, move_card, read_env_deatils
from todo_app.flask_config import Config
from todo_app.View_Class import ViewModel
from flask_login import LoginManager, login_required
from os import getenv
import requests
from requests import Response

def create_app():
    read_env_deatils()
    app = Flask(__name__)
    app.config.from_object(Config())
    login_manager = LoginManager()
    CLIENTID = getenv('CLIENTID')
    CLIENTSECRET = getenv('CLIENTSECRET')
    BASEURL = getenv('URL')
    STATE = getenv('STATE')

    @login_manager.unauthorized_handler
    def unauthenticated():
        url = f"https://github.com/login/oauth/authorize?client_id={CLIENTID}&state={STATE}&redirect_uri={BASEURL}/login/callback&allow_signup=true"
        return redirect(url)
    unauthenticated
    
    @login_manager.user_loader
    def load_user(user_id):
        pass # We will return to this later
    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        item_view_model = ViewModel(get_cards())
        return render_template('index.html', view_model=item_view_model, lists=get_lists())

    @app.route('/new', methods=['POST'])
    @login_required
    def new():
        add_card(request.form.get('title'))
        return redirect('/')

    @app.route('/move/<cardID>/<newList>')
    @login_required
    def move(cardID, newList):
        move_card(cardID, newList)
        return redirect('/')

    @app.route('/login/callback')
    #@login_required
    def callback():
        args = request.args
        request_token = args.get('code')
        url = f'https://github.com/login/oauth/access_token?client_id={CLIENTID}\&client_secret={CLIENTSECRET}&code={request_token}'
        headers = {'accept': 'application/json'}
        res = requests.post(url, headers=headers)
        data = res.json()
        print('mmmmmmmmmmmmm')
        print(args)
        print(request_token)
        print(url)
        print(data)
        
        print('mmmmmmmmmmmmm')
        access_token = data['access_token']
        access_token = 'token ' + access_token
        url = 'https://api.github.com/user'
        headers = {"Authorization": access_token}
        resp = requests.get(url=url, headers=headers)
        user_data = resp.json()
        #return render_template('success.html', userData=user_data)
        
        return redirect('/',userData=user_data)

    return app

