#!/usr/bin/env python3
""" Write a Python function that changes all topics of a school document
based on the name
"""


def update_topics(mongo_collection, name, topics):
    """ This return all topics of a achool document """
    filter_query = {"name": name}
    update_query = {"$set": {"topics": topics}}
    mongo_collection.update_many(filter_query, update_query)
