from db import db 

class ItemModel(db.Model):
	__tablename__ = 'items'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))

	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
	store = db.relationship('StoreModel')  # this replaces the SQL join


	def __init__(self, name, price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id 

	def json(self):
		return {'name': self.name, 'price': self.price}

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