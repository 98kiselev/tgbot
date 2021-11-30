from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# Create the client
client = MongoClient('localhost', 27017)

# Connect to our database
db = client['zakaz']

# Fetch our series collection
stol_collection = db['stol']


import json
from bson.objectid import ObjectId

def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__




@app.route('/')
def hello():
    return json.dumps(list(stol_collection.find()), default=newEncoder)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003)
