from app import app
from db import db

db.init_app(app)

# all tables will be created before the first request comes in 
@app.before_first_request
def create_tables():
	db.create_all()
	print('tables created')

