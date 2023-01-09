from mongodb import get_database
from pymongo.errors import CollectionInvalid
dbname = get_database()

# collection_static_room = dbname["room_static"]
def get_collection():
    user_schema = {
    'projector_availabilty': {
        'type': 'boolean',
        'minlength': 1,
        'required': True,
    },
    'room_number': {
        'type': 'string',
        'minlength': 1,
        'required': True,
    },
    'computer_availability': {
        'type': 'boolean',
        'minlength': 1,
        'required': True,
    },
    'no_seat': {
        'type': 'int',
        "required": True,
    },
    'wheelchair_friendly': {
        'type': 'boolean',
        'required': True,
    },
    'room_accebility': {
        'type': 'boolean',
        'required': True,
    },
    'airconditioning_availability': {
        'type': 'boolean',
        'required': True,
    },
    }
    collection_static_room = 'RoomStaticData'
    # The code bellow is used foe validation but we wont neede it cause mongob is nosql db
    # validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
    # required = []

    # for field_key in user_schema:
    #     field = user_schema[field_key]
    #     properties = {'bsonType': field['type']}
    #     minimum = field.get('minlength')

    #     if type(minimum) == int:
    #          properties['minimum'] = minimum

    #     if field.get('required') is True: required.append(field_key)

    #     validator['$jsonSchema']['properties'][field_key] = properties
    # if len(required) > 0:
    #         validator['$jsonSchema']['required'] = required

    # query = [('collMod',   collection_static_room),
    #               ('validator', validator)]

    # try:
    #      dbname.create_collection(collection_static_room)

    # except CollectionInvalid:
    #      pass
    #  USED TO CREAT A COLLECTION
    # dbname.create_collection(collection_static_room)
    return collection_static_room
#
if __name__ == "__main__":   
  
   # Get the database
   collection = get_collection()
   print(collection)