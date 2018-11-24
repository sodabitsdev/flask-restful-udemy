from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister 
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# turn off Flask_SQLAlchemy tracking off but keep underlying SQLAlchemy extension on
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False 
app.secret_key = "jose"
api = Api(app)


# all tables will be created before the first request comes in 
@app.before_first_request
def create_tables():
    db.create_all()
    print('tables created')


jwt = JWT(app, authenticate, identity)  # JWT creates a new endpoint /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')  # http://localhost:5000/student/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

# if we import app in another file then the Flask server will start.  So prevent from the server
# from starting up when we import app in another we add if the if statement below
# whichever file we run (i.e python <filename> ) then python internally calls that file __main__
# for that run.  So if we run this file, python app.py then python will call this file __main__
# when then will make the if statment below True and run the Flask server, otherwise the
# if statement is False and the Flask server will not start
if __name__ == '__main__':
    from db import db 
    db.init_app(app)
    app.run(port=5000, debug=True)
