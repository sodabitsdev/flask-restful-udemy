from db import db 

# Need to subclass db.Model so that SQLAlchemy will create the tables in the database
class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    # id is a python keyword so use _id
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod  # means we are using the current class 
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

        
    @classmethod  # means we are using the current class 
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
