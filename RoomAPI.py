from flask import Flask, jsonify, request, make_response
# from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from bson.objectid import ObjectId
from flask_swagger_ui import get_swaggerui_blueprint
from mongodb import get_database
from flask_restful import Resource, Api, reqparse
import json
from bson.json_util import dumps
from datetime import datetime
from mongodb import get_database
from collection import get_collection

# instantiate flask object
app = Flask(__name__)
api = Api(app)
dbname  =  get_database()
todos = dbname.room_static
collection = get_collection()
collection_room_static = dbname[collection]
# print(collection_room_static)
# print(collection_room_static.database)
ROOM = {}
room1 = {
  "room_number" : "aipS215",
  "projector_availability" : True,
  "room_accessibility" : True ,
  "no_seat" : 20,
  "airconditioning_availability" : True,
  "computer_availability": False,
  "wheelchair_friendly" : True,
}
# dbname.session.insert_one(room1)
collection_room_static.insert_one(room1)
print(room1)
# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Room List API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# instanctiate ma
ma = Marshmallow(app)
class RoomSchema(ma.Schema):
    class Meta:
        fields = ('projector_availabilty' , 
            'room_number' ,
            'room_accessibility' ,
            'no_seat" : no_seat',
            'airconditioning_availability',
            'computer_availability',
            'wheelchair_friendly',            
     )


# instantiate schema objects for todolist and todolists
room_schema = RoomSchema(many=False)
room_schema = RoomSchema(many=True)


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)
@app.route("/room", methods = ["POST"])
def add_todo():
    try:
        projector_availabilty = request.json ['projector_availabilty']
        room_number = request.json['room_number']
        room_accessibility = request.json['room_accessibility']
        no_seat = request.json['no_seat']
        airconditioning_availability = request.json['airconditioning_availability']
        computer_availability = request.json['computer_availability']
        wheelchair_friendly = request.json['wheelchair_friendly']
        
        new_Room = {
            "projector_availabilty" : projector_availabilty, 
            "room_number" : room_number,
            "room_accessibility" : room_accessibility ,
            "no_seat" : no_seat,
            "airconditioning_availability" :  airconditioning_availability,
            "computer_availability": computer_availability,
            "wheelchair_friendly" : wheelchair_friendly,            
        }
    
        collection_room_static.insert_one(new_Room)
        return room_schema.jsonify(new_Room)
    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again."})

# get all todos
@app.route("/room", methods = ["GET"])
def get_todos():
    item_details = collection_room_static.find()
   # This does not give a very readable output
    ROOM = json.loads(dumps(item_details, default=str))
    # todos = TodoList.query.all()
    # result_set = todolists_schema.dump(item_details)
    # print(result_set)
    return room_schema.jsonify(ROOM)



# get a specific todo
@app.route("/room/<id>", methods=["GET"])
def get_todo(id):
    # room_id  = room_id
    room = collection_room_static.find_one({"_id": id})
    # todo =  collection_room_static.query.get_or_404(int(id))
    return room_schema.jsonify(room)


# update a todo
@app.route("/todolist/<int:id>", methods=["PUT"])
def update_todo(id):

    room = collection_room_static.find_one({"_id": id})

    try:
        projector_availabilty = request.json ['projector_availabilty']
        room_number = request.json['room_number']
        room_accessibility = request.json['room_accessibility']
        no_seat = request.json['no_seat']
        airconditioning_availability = request.json['airconditioning_availability']
        computer_availability = request.json['computer_availability']
        wheelchair_friendly = request.json['wheelchair_friendly']
        
        room.projector_availabilty = projector_availabilty
        room.room_number = room_number
        room.room_accessibility = room_accessibility
        room.no_seat = no_seat
        room.airconditioning_availability = airconditioning_availability
        room.computer_availability =  computer_availability
        room.wheelchair_friendly = wheelchair_friendly
        dbname.session.update_one(room)
        return room_schema.jsonify(room)
    except Exception as e:
        return jsonify({"Error": "Invalid request, please try again."})   
   

# delete todo
@app.route("/todolist/<int:id>", methods=["DELETE"])
def delete_todo(id):
    room = collection_room_static.find_one({"_id": id})
    dbname.session.delete(room)
    dbname.session.commit()
    return jsonify({"Success" : "Todo deleted."})

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
     app.run(debug = True)
