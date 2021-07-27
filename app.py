import os
import re

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.stores import Store, StoreList

app = Flask(__name__)
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = ('uri', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'olya'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__': #when we import app.py on another file we dont want the app run on port 5000 everytime we import the file
    db.init_app(app)
    app.run(port=5000, debug=True) #when the app.py is main, meaning we are running app.py thats when Flask app will run
