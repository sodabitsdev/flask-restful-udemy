from db import db 

class StoreModel(db.Model):
	__tablename__ = 'stores'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	# this is List of items since it is a one-to-many relationship 
	# this is a backreference to the store
	# when every we get a story, SQLAlchemy will get all items related to the story unless we use lazy='dynamic'
	# the lazy='dynamic' indicates to SQLAlchemy not to get all of the items until we call. 
	# in method def json(self):  we call self.items.all() which gets all of the items for this store
	items = db.relationship('ItemModel', lazy='dynamic') 
	


	def __init__(self, name):
		self.name = name
		

	def json(self):
		return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

	@classmethod
	def find_by_name(cls, name):
		# this is saying 'SELECT * FROM ITEMS WHERE NAME=?
		#return ItemModel.query.filter_by(name=name) - ALTERNATIVE replace ItemModel with cls
		return cls.query.filter_by(name=name).first()
	
	
	def save_to_db(self):
		# insert or update to the database, upsert
		db.session.add(self)
		db.session.commit()


	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()