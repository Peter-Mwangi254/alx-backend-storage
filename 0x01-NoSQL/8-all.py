#!/usr/bin/env python3
"""
Write a Python function that lists all documents in a collection:
"""


import pymongo


def list_all(mongo_collection):
    """Return list of all docs in collection"""
    if mongo_collection is None:
        return []
    docs = mongo_collection.find()
    return [doc for doc in docs]
