#!/usr/bin/env python3
"""Write a Python function that inserts a new document
in a collection based on kwargs:
Returns the new _id
"""


import pymongo


def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection"""
    return mongo_collection.insert(kwargs)
