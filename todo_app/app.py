from flask import Flask, redirect, render_template, request
from todo_app.data.trello_items import add_card, get_cards, get_lists, move_card, read_env_deatils
from todo_app.flask_config import Config
from todo_app.View_Class import ViewModel
from flask_login import LoginManager, login_required, login_user
from os import getenv
import requests
from todo_app.data.user_class import User

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
        recivedCode = args.get('code')
        url = f'https://github.com/login/oauth/access_token?client_id={CLIENTID}&redirect_uri={BASEURL}/login/callback&client_secret={CLIENTSECRET}&code={recivedCode}'
        headers = {'Accept': 'application/json'}
        resp = requests.post(url=url, headers=headers)
        data = resp.json()
        access_token = data['access_token']
        tempAT = 'Bearer '+access_token
        url2 = 'https://api.github.com/user'
        headers2 = {"Authorization": tempAT}
        resp2 = requests.get(url=url2, headers=headers2)
        user_data = resp2.json()
        thisuser = User(user_data['id']) 
        login_user(thisuser, remember=False, duration=None, force=True, fresh=True)
        who = load_user(thisuser)
        print(who)
        return redirect('/')

# upto step 3.5 ##########################################################
#{'login': 'wishy78', 'id': 65459782, 'node_id': 'MDQ6VXNlcjY1NDU5Nzgy', 'avatar_url': 'https://avatars.githubusercontent.com/u/65459782?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/wishy78', 
#'html_url': 'https://github.com/wishy78', 'followers_url': 'https://api.github.com/users/wishy78/followers', 'following_url': 'https://api.github.com/users/wishy78/following{/other_user}', 'gists_url': 'https://api.github.com/users/wishy78/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/wishy78/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/wishy78/subscriptions', 'organizations_url': 'https://api.github.com/users/wishy78/orgs', 'repos_url': 'https://api.github.com/users/wishy78/repos', 'events_url': 'https://api.github.com/users/wishy78/events{/privacy}', 'received_events_url': 'https://api.github.com/users/wishy78/received_events', 'type': 'User', 'site_admin': False, 'name': None, 'company': None, 'blog': '', 'location': None, 'email': None, 'hireable': None, 'bio': None, 'twitter_username': None, 'public_repos': 9, 'public_gists': 0, 'followers': 0, 'following': 0, 'created_at': '2020-05-16T16:23:41Z', 'updated_at': '2022-09-29T09:36:17Z'}
    return app

