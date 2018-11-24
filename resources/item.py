from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# the Api works with Resources and every Resource has to be a class
# we no longer have to jsonify since flask_restful returns a dictionary

class Item(Resource):
	# the Http request attribues are accessible through the reqparse.RequestParser()
	# parser at the class level will make it available to all methods
	parser = reqparse.RequestParser()

	# Need to add an argument for each parameter I expect to recieve.  In this class we only
	# expect to retrieve the price parameter from the Http request 
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field cannot be left blank!"
	)

	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every item needs a store id"
	)


	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		
		return {'message': 'Item not found'}, 404


	def post(self, name):
		if ItemModel.find_by_name(name):
			return {'message': "An item with '{}' already exists.".format(name)}, 400

		# if payload is not json it will give you an error
		data = Item.parser.parse_args()

		item = ItemModel(name, data['price'], data['store_id'])
		# the above line could have been written as the line below
		# item = ItemModel(name, **data)

		try:
			item.save_to_db()
		except:
			return {"message": "An error occurred inserting the item"}, 500 # Internal Server Error
		
		# HTTP 201 is for created
		return item.json(), 201   


	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		
		return {'message': 'Item deleted'}


	def put(self, name):
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		
		if item is None:
			item = ItemModel(name, data['price'], data['store_id'])
			# the above line could have been written as the line below
			# item = ItemModel(name, **data)
		else:
			item.price = data['price']

		item.save_to_db()

		return item.json()





class ItemList(Resource):
	def get(self):
		# look up list comprehension 
		return {'items': [item.json() for item in ItemModel.query.all()]}

		# lambda way
		# return 'items': list(map(lambda x: x.json(), ItemModel.query.all()))


