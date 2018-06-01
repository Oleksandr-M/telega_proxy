#!bin/python

from app import app
app.run(host='0.0.0.0', debug = True, ssl_context=('fullchain.pem', 'privkey.pem'), port = 443)

