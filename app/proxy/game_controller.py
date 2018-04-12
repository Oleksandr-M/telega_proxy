import json
from app import db
from app.models import EnGame, EnLvl, EnSectors
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.game_managment import edit_game_name, get_domain, get_game_id


def en_game_info_create(page, user_id):
    return 1

def en_game_logger (proxy_key, page_json):
    print (page_json)
    if page_json['levelinfo'] == False:
        return 0
    #print ('game id ='+str(get_game_id(proxy_key)))
    # створення нової гри
    if EnGame.query.filter_by (en_game_id = get_game_id(proxy_key), proxy_key = proxy_key).count()==0:
        print ('new game found')
        game = EnGame (get_game_id(proxy_key), proxy_key)
        db.session.add (game)
        try:
            db.session.commit()
        except:
            print ('помилка створення нового сценарю гри')
            db.session.rollback()
    # створення нового рівня
    levelInfo = json.loads(page_json ['levelinfo'])
    #print (levelInfo['levelId'])
    if EnLvl.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).count() == 0:
        lvl = EnLvl (get_game_id(proxy_key), levelInfo['levelId'], levelInfo['levelNum'])
        db.session.add(lvl)
        #print ('new level found')
        try:
            db.session.commit()
            en_level_info_updater (proxy_key, page_json)
        except:
            db.session.rollback()
            print('помилка створення новго рівня гри')
    else:
 #       lvl = EnLvl.query.filter_by(en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).first()
        en_level_info_updater (proxy_key, page_json)
        print ('old level found')
        #print (lvl)

    return 1

def en_level_info_updater (proxy_key, pageJson):
    levelInfo = json.loads(pageJson ['levelinfo'])
    lvl = EnLvl.query.filter_by(en_game_id = get_game_id(proxy_key), en_lvl_id = levelInfo['levelId'], en_lvl_no = levelInfo['levelNum']).first()
    # TODO перевірка чи нічого не змінилося в рівні і додавання в сигнали боту
    lvl.en_answer_block = pageJson['block']
    sectors_counter = json.loads(pageJson['sectors_count'])
    lvl.en_sectors_count = sectors_counter['all']
    lvl.en_sectors_need =  sectors_counter ['need']
    sectors_counter = json.loads (pageJson['sectors_info'])
    
    en_sectors_logger (proxy_key, levelInfo['levelId'], levelInfo['levelNum'], sectors_counter)
    closed = 0
    for sector in sectors_counter:
        if sector['entered']:
            closed +=1
    lvl.en_sectors_closed = closed
    try:
            db.session.commit()
    except:
            db.session.rollback()
            print ('Помилка оновлення даних рівня')
    return None

def en_sectors_logger (proxy_key, en_lvl_id, en_lvl_no, sectorsJson):
    # TODO перевірка чи не змінилась кількість секторів і їх назви і закритість
    print ('sectors' + str(sectorsJson))
    
    print ('sectors count'+ str (sectors_counter(sectorsJson)))

    print ('sectors in DB ' + str(EnSectors.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = en_lvl_id, en_lvl_no = en_lvl_no).count()))

    print_sectors_from_db (proxy_key, en_lvl_id, en_lvl_no)

    # якщо ще не внесені сектори в рівень то створюємо нові
    if EnSectors.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = en_lvl_id, en_lvl_no = en_lvl_no).count() == 0:
        print ('no sectors was logged!!!') #TODO повідомлення про додавання секторів
        counter = 1
        for sectors in sectorsJson:
            print ('sector #' + str(counter) + ' name = '+ sectors['name'])
            en_sector = EnSectors(get_game_id(proxy_key), 
                                  en_lvl_id, 
                                  en_lvl_no, 
                                  counter, 
                                  sectors['name'],
                                  sectors['entered'],
                                  sectors['answer'],
                                  sectors['gamer'])
            db.session.add(en_sector)
            db.session.commit()
            try:
                
                counter +=1
                print ('sector added')
            except:
                db.session.rollback()
                print ('sector adding error')
    #Якщо вже є сектори то перевіряємо чи кількість не змінилася
    else:
        if EnSectors.query.filter_by (en_game_id = get_game_id(proxy_key), en_lvl_id = en_lvl_id, en_lvl_no = en_lvl_no).count() != sectors_counter(sectorsJson):
            #TODO повідомлення про зміну кількості секторів
            print ('level sectors coutn was changed!!!')
            counter = 1
            for sector in sectorsJson:

                if EnSectors.query.filter_by(en_game_id = get_game_id(proxy_key), 
                                            en_lvl_id = en_lvl_id, 
                                            en_lvl_no = en_lvl_no, 
                                            en_sector_no = counter).all().count() == 0:
                    print ('sector was added')
                    en_sector = EnSectors(get_game_id(proxy_key), 
                                  en_lvl_id, 
                                  en_lvl_no, 
                                  counter, 
                                  sectors['name'],
                                  sectors['entered'],
                                  sectors['answer'],
                                  sectors['gamer'])
                    db.session.add(en_sector)
                    db.session.commit()
                    try:
                        db.session.commit()
                        counter +=1
                        print ('sector added')
                    except:
                        db.session.rollback()
                        print ('sector adding error')
    # інформація про сектори поновляється в будь якому випадку
    print ('level sectors info updating')
    counter = 1
    print ('------------------------START update sector printing -------------------')
    for sectors in sectorsJson:
    print (sectors)
        updated = False
        en_sector = EnSectors.query.filter_by(en_game_id = get_game_id(proxy_key), 
                                  en_lvl_id = en_lvl_id, 
                                  en_lvl_no = en_lvl_no, 
                                  en_sector_no = counter).first()
        if sectors['name'] != en_sector.en_sector_name:
            print ('sector #' + str(counter) + ' name was changed to ' + str(sectors['name']))
            # TODO сигнал боту про зміну назви сектора
            updated = True
            en_sector.en_sector_name = sectors['name']
        if sectors ['entered'] != en_sector.en_sector_entered:
            # TODO сигнал боту про введення сектора
            print ('sector #' + str(counter) + ' name was closed by code ' + sectors['answer'] + ' by gamer '+ sectors['gamer'])
            updated = True
            en_sector.en_sector_entered = True
            en_sector.en_sector_answer = sectors['answer']
            en_sector.en_gamer = sectors['gamer']
        if updated:
            try:
                db.session.commit()
                counter +=1
                print ('sector updated #' + str (counter))
            except:
                db.session.rollback()
                print ('sector updating error')
    print ('------------------------END update sector printing -------------------')
    return None

def sectors_counter (sectorsJson):
    counter = 0
    for sector in sectorsJson:
        counter +=1
    return counter

def print_sectors_from_db (proxy_key, en_lvl_id, en_lvl_no):
    sectors = EnSectors.query.filter_by (en_game_id = get_game_id(proxy_key), 
                                         en_lvl_id = en_lvl_id, 
                                         en_lvl_no = en_lvl_no).all()
                                         
    print ('------------------------START DB sectors printing -------------------')
    print (sectors)                                        
    for sector in sectors:
        print ('sector No:' + str(sector.en_sector_no)+ ' sector name ' + sector.en_sector_name + ' closed:' + str(sector.en_sector_entered) + ' answer: '+ sector.en_sector_answer + ' gamer: ' + sector.en_gamer)
    print ('------------------------END DB sectors printing -------------------')
    return None
                                  


