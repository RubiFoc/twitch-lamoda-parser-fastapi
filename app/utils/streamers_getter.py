import uuid


def serialize_document(document):
    if 'id' in document:
        document['_id'] = str(document['_id'])