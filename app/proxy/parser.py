import json
import time
from bs4 import BeautifulSoup
from datetime import datetime


"""
left_panel_tag ='tdContentLeft'
header_tag = 'tableHeader'
right_panel_tag ='tdContentRight'
main_manu_tag = 'menuWrap'
info_block ='boxCenterContent'
vote_class ='enPnl1 border_rad2 clr2'
discuss_class ='discuss'
game_info_class =  'lnkGameTitle' #'boxGameInfo' 'yellow_darkgreen19'
game_info_table_class = 'gameInfo'
"""

game_name_id = 'lnkGameTitle'
game_start_time_id = 'ComingGamesRepeater_ctl00_gameInfo_enContPanel_lblYourTime'
game_description_class = 'divDescr'
level_id_name = 'LevelId'
level_number_name = 'LevelNumber'
history_class = 'history'
correct_answer_class ='color_correct'
correct_bonus_class = 'color_bonus'

def get_game_info(page):
    soup = BeautifulSoup(page.text)
    name =soup.find('a', id = game_name_id).get_text()

    #soup = BeautifulSoup(page.text)
    #time = soup.find('span', id = game_start_time_id).get_text()
#    soup = BeautifulSoup(page.text)
#    description = soup.find ('div', class_ = game_description_class).prettify()
#    info = {'name':name,'description':description}
    
    print (soup.prettify())
    
    return name

def change_href (page, id):
    soup = BeautifulSoup(page.text)
    soup.prettify()
    for ref in soup.findAll('a', href=True):
        if ref['href'][0] == '/':
            ref['href'] = '/proxy/'+str(id)+ref['href']
    for ref in soup.findAll('a', href=True):
        print (ref['href'])
    return soup.prettify()

def level_parser (page):
    soup = BeautifulSoup(page)
    soup.prettify()
    print (get_level_num (soup))
    print (get_level_history (soup))
    return page

def get_level_num (pageSoup):
    """
    отримує суп сторінки гри, повертає json:
    {'levelId':id рівня в ігровій системі,
    'levelNum':номер рівня в ігрі}
    """
    inputs = pageSoup.find('form').findAll('input')
    for input_ in inputs:
        if input_.has_attr('name'):
            if input_['name'] == level_id_name:
                level_id = input_['value']
            if input_['name'] == level_number_name:
                level_num = input_['value']
    print (level_id, level_num)
    return json.dumps ( {'levelId':level_id,
                    'levelNum':level_num })

def get_level_history (pageSoup):
    history = []
    history_list = pageSoup.find('ul', class_=history_class)
    items = history_list.findAll('li')
    for item in items:
        code_date = get_code_date(item.get_text().strip())
        #code_date = code_date[0:code_date.find('/n')]
        print (str(code_date))
        user = item.find('a').get_text().strip()
        answer = item.find('span').get_text().strip()
        answer_class = item.find('span')['class']
        print ('answer class =' +str(answer_class))
        if  answer_class[0] == correct_answer_class:
            correct = True
            isCode = True
        else:
            if answer_class[0] == correct_bonus_class:
                correct = True
                isCode = False
            else:
                correct = False
                isCode = True

        history.append ({'time':code_date,'gamer':user,'answer':answer,'correct':correct,'is_code':isCode})
        
        #print (item.get_text())
    #print (history_list)
    return json.dumps(history)

def get_code_date(inStr):
    tmp_date_str = str(datetime.now().year)+'/'+inStr.split()[0]+' '+ inStr.split()[1]
    tmp_date_str = tmp_date_str.replace ('/', ' ')
    date = datetime.strptime (tmp_date_str, '%Y %d %m %H:%M:%S')
    return time.mktime (date.timetuple())
