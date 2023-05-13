from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util
import os
import json


app = Flask(__name__)
client = MongoClient(os.getenv("MONGO"))
db = client['pypi-packages']
pypipackages = db['pypi_packages']
print(json.loads(json_util.dumps(pypipackages.find())))

pypipackages.delete_many({})