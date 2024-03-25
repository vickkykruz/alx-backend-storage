#!/usr/bin/env python3
""" Write a Python function that inserts a new document in a collection
based on kwargs:
"""


def insert_school(mongo_collection, **kwargs):
    """ This function return the inserted document """
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    # Return the new _id
    return result.inserted_id
