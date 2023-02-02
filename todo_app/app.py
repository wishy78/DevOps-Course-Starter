from flask import Flask, redirect, render_template, request
from todo_app.data.mongo_items import add_card, get_cards, get_lists, move_card, read_env_deatils, get_myrole, get_currentuser
from todo_app.flask_config import Config
from todo_app.View_Class import ViewModel
from flask_login import LoginManager, login_required, login_user, current_user
from os import getenv
import requests
from todo_app.data.user_class import User
from datetime import timedelta



def create_app():
    read_env_deatils()
    app = Flask(__name__)
    app.config.from_object(Config())
    login_manager = LoginManager()
    CLIENTID = getenv('CLIENTID')
    CLIENTSECRET = getenv('CLIENTSECRET')
    BASEURL = getenv('URL')
    STATE = getenv('STATE')
    app.config['LOGIN_DISABLED'] = getenv('LOGIN_DISABLED') == 'True'

    @login_manager.unauthorized_handler
    def unauthenticated():
        url = f"https://github.com/login/oauth/authorize?client_id={CLIENTID}&state={STATE}&redirect_uri={BASEURL}/login/callback&allow_signup=true"
        return redirect(url)
    
    @login_manager.user_loader
    def load_user(user_id):
       #pass # We will return to this later
        thisuser = User(user_id)
        return (thisuser)
    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        item_view_model = ViewModel(get_cards())
        return render_template('index.html', view_model=item_view_model, lists=get_lists(), user1=get_currentuser(), role=get_myrole(get_currentuser().id))

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

    @app.route('/role/<UserID>')
    @login_required
    def myrole(UserID):
        myroles(UserID)
        return redirect('/')

    @app.route('/login/callback')
    #@login_required
    def callback():
        #args = request.args
        #recivedCode = args.get('code')
        recivedCode = request.args.get('code')
         
        url = f'https://github.com/login/oauth/access_token?client_id={CLIENTID}&redirect_uri={BASEURL}/login/callback&client_secret={CLIENTSECRET}&code={recivedCode}'
        headers = {'Accept': 'application/json'}
        #resp = requests.post(url=url, headers=headers)
        #data = resp.json()
        #access_token = data['access_token']
        access_token = requests.post(url=url, headers=headers).json()['access_token']
        #print(requests.post(url=url, headers=headers).json())
        tempAT = 'Bearer '+access_token
        url2 = 'https://api.github.com/user'
        headers2 = {"Authorization": tempAT}
        #resp2 = requests.get(url=url2, headers=headers2)
        #user_data = resp2.json()
        #thisuser = User(user_data['id']) 
        #thisuser = User(requests.get(url=url2, headers=headers2).json()['id']) 
        thisuser = User(requests.get(url=url2, headers=headers2).json()) 
        duration1 = timedelta(seconds=60)
        login_user(thisuser['id'], remember=False, duration=duration1, force=True, fresh=True)
        who = load_user(thisuser['name'])
        print(who)
        return redirect('/')
    return app
