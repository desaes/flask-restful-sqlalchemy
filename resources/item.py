from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True, 
        help="This field cannot bet left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True, 
        help="Every item needs a store id."
    )    

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exist.".format(name)}, 400 # bad request -> 400

        request_data = Item.parser.parse_args()
        #request_data = request.get_json(force=true) # if content type is not setted to json, it forces the parsing, not recomended
        #request_data = request.get_json(silent=True) # basically return none if content type is not setted to json
 
        item = ItemModel(name, **request_data)
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500 # Internal server error

        return item.json(), 201 # created -> 201
                                # accepted -> 202, used when queueing operations0

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}

        return {'message': "Item with name {} not found.".format(name)}, 400 # bad request -> 400

    def put(self, name):
        #request_data = request.get_json(silent=True) # basically return none if content type is not setted to json
        request_data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json(), 201
         

class ItemList(Resource):
    def get(self):
        # using list comprehentions
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # or
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
