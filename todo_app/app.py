from flask import Flask, redirect, render_template, request
from todo_app.data.mongo_items import add_card, get_cards, get_lists, move_card, read_env_deatils, get_myrole, get_currentuser, role_required
from todo_app.flask_config import Config
from todo_app.View_Class import ViewModel
from flask_login import LoginManager, login_required, login_user
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
        user_name = user_id.split(",")[0].split(":")[1].replace("'","")
        user_id = user_id.split(",")[1].split(":")[1].replace("'","")
        thisuser = User(user_id,user_name)
        return (thisuser)
    login_manager.init_app(app)

    @app.route('/')
    @login_required
    def index():
        item_view_model = ViewModel(get_cards())
        ThisUser = get_currentuser()
        return render_template('index.html', view_model=item_view_model, lists=get_lists(), user1=ThisUser, role=get_myrole(ThisUser.id))

    @app.route('/new', methods=['POST'])
    @login_required
    #@role_required('writer')
    def new():
        if role_required('writer') :
            exit
        add_card(request.form.get('title'))
        return redirect('/')

    @app.route('/move/<cardID>/<newList>')
    @login_required
    #@role_required('writer')
    def move(cardID, newList):
        if role_required('writer') :
            exit
        move_card(cardID, newList)
        return redirect('/')

    @app.route('/login/callback')
    def callback():
        recivedCode = request.args.get('code')
        url = f'https://github.com/login/oauth/access_token?client_id={CLIENTID}&redirect_uri={BASEURL}/login/callback&client_secret={CLIENTSECRET}&code={recivedCode}'
        headers = {'Accept': 'application/json'}
        response1 = requests.post(url=url, headers=headers).json()
        accesstoken = response1['access_token']
        accesstokenstr = 'Bearer '+accesstoken
        url2 = 'https://api.github.com/user'
        headers2 = {"Authorization": accesstokenstr}
        response = requests.get(url=url2, headers=headers2).json()
        thisuser = User(response,response['login']) 
        duration1 = timedelta(seconds=60)
        #print(thisuser.id['id'])
        #print(thisuser.id['login'])
        login_user(thisuser, remember=False, duration=duration1, force=True, fresh=True)
        return redirect('/')
    return app
