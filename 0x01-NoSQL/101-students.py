#!/usr/bin/env python3
""" Write a Python function that returns all students sorted by average
 score:
"""


def top_students(mongo_collection):
    """ This return all the students storted by average """
    pipeline = [
            {"$unwind": "$topics"},
            {
                "$group": {
                    "_id": "$_id", "name": {
                        "$first": "$name"
                        },
                    "averageScore": {
                        "$avg": "$topics.score"
                        }
                    }
                },
            {
                "$sort": {
                    "averageScore": -1
                    }
                }
            ]

    results = mongo_collection.aggregate(pipeline)
    return list(results)
