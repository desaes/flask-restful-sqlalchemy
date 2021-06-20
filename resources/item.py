import sqlite3
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
 
        item = ItemModel(name, request_data['price'])
        
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item"}, 500 # Internal server error

        return item.json(), 201 # created -> 201
                                # accepted -> 202, used when queueing operations0

    def delete(self, name):
        if ItemModel.find_by_name(name):
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()            

            return {'message': 'Item deleted'}

        return {'message': "Item with name {} not found.".format(name)}, 400 # bad request -> 400

    def put(self, name):
        #request_data = request.get_json(silent=True) # basically return none if content type is not setted to json
        request_data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, request_data['price'])
        
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item"}, 500 # Internal server error
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item"}, 500 # Internal server error
        return updated_item.json(), 201
         

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()      

        return {'items': items}     
