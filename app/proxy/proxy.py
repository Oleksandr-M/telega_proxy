import requests
from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g
from jinja2 import TemplateNotFound
from flask_login import login_user, logout_user, current_user, login_required
import app
from app.proxy.parser import get_game_info, change_href
from app.game_managment import edit_game_name, get_domain, get_game_id
from app.models import Proxy


def get_session(proxy):
    for session in app.game_session:
        if session['proxy'] == proxy:
            return session['session']

proxy = Blueprint('proxy', 'proxy', template_folder='templates')


@proxy.route('/')
@login_required
def show():
    return render_template ('index.html', user = current_user)

@proxy.route('/proxy_creator/<id>')
@login_required
def proxy_creator(id):
    domain = request.args.get('domain')
    proxy_key = request.args.get('proxy')
    login = request.args.get('login')
    password = request.args.get('password')
    r = requests.Session()
    app.game_session.append ({'game':id,'proxy':proxy_key,'session':r})
    page = r.get('http://'+domain+'/GameDetails.aspx?gid='+str(id))
    edit_game_name (id,  get_game_info (page))
    login_page = r.get ('http://'+domain+'/Login.aspx?login='+login+'&password='+password)
    
    return redirect(url_for(request.args.get ("redirect_url")))


@proxy.route('/<id>', methods=['GET'])
@login_required
def en_game_proxy_root(id):
    r = get_session (id)
    url = 'http://'+get_domain(id)+'/gameengines/encounter/play/'+get_game_id(id)
    return change_href(r.get (url),id)


@proxy.route('/<id>/<path:path>', methods=['GET'])
@login_required
def en_game_proxy_get(id,path):
    r = get_session (id)
    url = 'http://'+get_domain(id)+'/'+path
    return change_href(r.get (url),id)

@proxy.route('/<id>/<path:path>', methods=['POST'])
@login_required
def en_game_proxy_post(id,path):
        print(request.form.to_dict())
        r = get_session (id)
        url = 'http://'+get_domain(id)+'/'+path
        return change_href(r.get (url),id)

@proxy.route('/<id>', methods=['POST'])
@login_required
def en_game_proxy_post_root(id):
        print(request.form.to_dict())
        r = get_session (id)
        url = 'http://'+get_domain(id)+'/gameengines/encounter/play/'+get_game_id(id)
        return change_href(r.get (url),id)
    




