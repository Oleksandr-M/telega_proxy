from app.models import Game
from sqlalchemy.orm import sessionmaker
from app import db

def new_game (domain, id, name, gamer, chat, owner):
    new_game = Game (domain, id, name, gamer, chat, owner)
    db.session.add (new_game)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        print ('Помилка запису параметрів гри у базу')
        return 'Помилка запису параметрів гри у базу'

def active_games_list (owner = 0):
    if owner ==0 :
        return Game.query.all()
    else:
        return Game.query.filter_by(owner = owner).all()

def delete_game (id):
    game = Game.query.filter_by (id=id).first()
    db.session.delete(game)
    try:
        db.session.commit()
        return 1
    except:
        db.session.rollbac()
        return 'помилка видалення гри'
