from pymongo.cursor import Cursor


def serialize(objects: Cursor):
    object_list = []
    for object in objects:
        object['_id'] = str(object['_id'])
        object_list.append(object)

    return object_list