from flask import Flask, redirect, render_template, request, session
from todo_app.data.mongo_items import add_card, get_cards, get_lists, move_card, read_env_deatils, get_myrole, get_currentuser, randStr
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
    app.config['LOGIN_DISABLED'] = getenv('LOGIN_DISABLED') == 'True'

    @login_manager.unauthorized_handler
    def unauthenticated():
        state = randStr(N=20)
        session['state'] =state
        url = f"https://github.com/login/oauth/authorize?client_id={CLIENTID}&state={state}&redirect_uri={BASEURL}/login/callback&allow_signup=true"
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

    def is_writer():
        ThisUser = get_currentuser()
        UserRole = get_myrole(ThisUser.id)
        return UserRole == "writer"

    @app.route('/new', methods=['POST'])
    @login_required
    def new():
        if not is_writer():
            raise Exception("You dont have write access")
        add_card(request.form.get('title'))
        return redirect('/')

    @app.route('/move/<cardID>/<newList>')
    @login_required
    def move(cardID, newList):
        if not is_writer():
            raise Exception("You dont have write access")
        move_card(cardID, newList)
        return redirect('/')

    @app.route('/login/callback')
    def callback():
        recivedCode = request.args.get('code')
        state = request.args.get('state')
        if (session['state'] != state):
            raise Exception("State does not match; indicates referral from a different hostname")
        url = f'https://github.com/login/oauth/access_token?client_id={CLIENTID}&redirect_uri={BASEURL}/login/callback&client_secret={CLIENTSECRET}&code={recivedCode}'
        headers = {'Accept': 'application/json'}
        response1 = requests.post(url=url, headers=headers).json()
        accesstoken = response1['access_token']
        accesstokenstr = 'Bearer '+accesstoken
        url2 = 'https://api.github.com/user'
        headers2 = {"Authorization": accesstokenstr}
        response = requests.get(url=url2, headers=headers2)
        response.raise_for_status()
        Jsonresponse = response.json()
        thisuser = User(Jsonresponse,Jsonresponse['login']) 
        duration1 = timedelta(seconds=3600)
        login_user(thisuser, remember=False, duration=duration1, force=True, fresh=True)
        return redirect('/')
    return app