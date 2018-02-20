from hashlib import md5
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

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



