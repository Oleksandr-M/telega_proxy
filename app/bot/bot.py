from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from jinja2 import TemplateNotFound
from bs4 import BeautifulSoup, Tag

import app
import telepot
import json
from app import db
from app.models import Chat, botSignall, Chat_opt

bot = Blueprint('bot', 'bot', template_folder='templates')

telegram_api_key = '603679580:AAHtJ6he-CTCfv-aVtUiipAedc6l6_IxrZY'

telega_bot = telepot.Bot(telegram_api_key)
telega_bot.setWebhook('https://proxy-telega.a3c1.starter-us-west-1.openshiftapps.com/bot/{}'.format(telegram_api_key))


@bot.route('/'+telegram_api_key, methods=['POST', 'GET'])
def message_listener():
    update = request.get_json() #TODO перевірку чи такий чат є в базі якщо немає то створити
    find_chat(update)
    read_signals (get_chat_id_from_update (update))
    return 'bot ok'

def find_chat (json_plain):
    
    jsonIn = json_plain
    print (jsonIn)
    message = jsonIn ['message']
    chat = message['chat']
    if Chat.query.filter_by(tg_id = int(chat['id'])).count() ==0:
        if chat['type']!='private':
            chat_db = Chat(chat['id'], chat['title'], "<img></img>",0)
        else:
            message = jsonIn['message']
            user = message['from']
            privat_title = 'Private chat with {}'.format(user['username'])
            chat_db = Chat(chat['id'], privat_title, "<img></img>",0) 
        chat_opt = Chat_opt (chat_db.tg_id)
        db.session.add(chat_db)
        db.session.add(chat_opt)
        try:
            db.session.commit()
            print ('new chat added')
        except:
            db.session.rollback()
            print ('error while adding chat to db')
    
    return None

def read_signals (chat_id):
        signals = botSignall.query.filter_by (chat_id = chat_id).order_by(botSignall.level.asc(), botSignall.signal_date.asc()).all()
        if len(signals) == 0:
            return None
        for signal in signals:
           # print(signal)
            if signal.signal_type == 5:
                message = json.loads(signal.signal_json)
                send_html_message (chat_id, message)
                #telega_bot.sendMessage (chat_id, message['msg'] + message['html'])
                db.session.delete (signal)
            if signal.signal_type == 8:
                message = json.loads(signal.signal_json)
                telega_bot.sendMessage (chat_id, message['msg'])
                db.session.delete (signal)
            if signal.signal_type == 2:
                message = json.loads(signal.signal_json)
                telega_bot.sendMessage (chat_id, message['msg'] + message['html'])
                db.session.delete (signal)
            if signal.signal_type == 12:
                message = json.loads(signal.signal_json)
                telega_bot.sendMessage (chat_id, message['msg'] + message['html'])
                db.session.delete (signal)
                #db.session.delete(signall)
                #db.session.commit()
            if signal.signal_type == 13:
                message = json.loads(signal.signal_json)
                telega_bot.sendMessage (chat_id, message['msg'] + message['html'])
                db.session.delete (signal)
            if signal.signal_type == 16:
                message = json.loads(signal.signal_json)
                telega_bot.sendMessage (chat_id, message['msg'] + message['html'])
                db.session.delete (signal)
            if signal.signal_type == 17:
                message = json.loads(signal.signal_json)
                telega_bot.sendMessage (chat_id, message['msg'] + message['html'])
                db.session.delete (signal)
            db.session.commit()
            
            
            
            
        return None

def get_chat_id_from_update (jsonIn):
    message = jsonIn ['message']
    chat_id = message ['chat']['id']
    return chat_id

def send_html_message (chat_id, messageJson):
    soup = BeautifulSoup (messageJson['html']).prettify()
   
    html = ''
    print (soup)
    html_dic = []
    for line in soup.split('\n'):
        if line.find('div') >0:
            line = ''
        if line.find('span') >0:
            line = ''
        if line.find('<br/>') > 0:
            line = '\n'
        if line.find('<html>') > 0:
            line = ''
        if line.find('</html>') > 0:
            line = ''
        if line.find('<body>') > 0:
            line = ''
        if line.find('</body>') > 0:
            line = ''
        if line.find('<p>') >0:
            line = '/n'
        if line.find('</p>') >0:
            line = ''
        if line.find('<h3>') > 0:
            line = '<b>'
        if line.find('</h3>') > 0:
            line = '</b>'
        if line !='': 
            html_dic.append(line.strip())
    html_dic.remove('<html>')
    html_dic.remove('</html>')
    
      
    
    print (html_dic)
    html = '<b>' + messageJson['msg'] + '</b> \n'
    for item in html_dic:
        if item.find('<img') > 0:
            telega_bot.sendMessage (chat_id, html, parse_mode = 'HTML')
            html =  ''
            img = BeautifulSoup (item)
            for tag in img.findAll (itemprop="image"):
                telega_bot.sendPhoto (chat_id, tag['src'])
            item = ''
        html = html+item
    
    
    return None
