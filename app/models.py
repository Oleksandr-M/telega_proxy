from hashlib import md5
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1
ROLE_SUPERUSER = 2

TELEGA_USER = 0
TELEGA_ADMIN = 1
TELEGA_SUPERUSER = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(120), index = True, unique = False)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __init__ (self, login, email, password , role):
        self.login = login
        self.email = email
        self.password = password
        self.role = role
        

    def __repr__(self):
        return '<User %r>' % (self.login)
        
    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode()).hexdigest() + '?d=mm&s=' + str(size)


class Gamers (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index = True, unique = False)
    password = db.Column(db.String(120), index = True, unique = False)
    comment = db.Column(db.String(120), index = True, unique = False)
    creator_id = db.Column(db.Integer)    
    
    def __repr__(self):
        return '<User %r>' % (self.login)

    def __init__ (self, login, password , comment,  creator_id):
        self.login = login
        self.password = password
        self.comment = comment
        self.creator_id = creator_id

class Telegram_Users (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tg_login = db.Column(db.String(64), index = True, unique = True)
    tg_id = db.Column(db.String(64), index = True, unique = True)
    telega_id = db.Column(db.Integer,index = True, unique = False)
    telega_role = db.Column(db.SmallInteger, default = TELEGA_USER)
    creator_id = db.Column(db.Integer)    
    
    def __repr__(self):
        return '<User %r>' % (self.tg_login)

    def __init__ (self, tg_login, tg_id , telega_id,  telega_role, creator_id):
        self.tg_login = tg_login
        self.tg_id = tg_id
        self.telega_id = telega_id
        self.telega_role = telega_role
        self.creator_id = creator_id