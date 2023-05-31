import os
import requests
import subprocess
import shutil
import pymongo
from pymongo import MongoClient
import configparser

API_URL = os.getenv("PYPIAPI")
MONGO_URI = os.getenv("MONGO")
AITOKEN = os.getenv("OPENAI_API_KEY")

# Create a MongoDB client
client = MongoClient(MONGO_URI)
db = client['pypi-packages']


def filenames(mypath):
  file_names = []
  files = os.listdir(mypath)
  for file in files:
    file_names.append(file)
  return file_names


if __name__ == "__main__":
  query = {'sourcedownloaded': True, 'sourceunpacked': True, 'specfilecreated': False}
  packages = db['pypi_packages']
  for package in packages.find(query):
    myname = package['name']
    myversion = package['version']
    downloadpath = os.getenv("DOWNLOADPATH")
    downloadpath = downloadpath + "/" + str(myname) + "-" + str(myversion)
    print(downloadpath)
    if os.path.exists(downloadpath):
      print("Directory exists")
    else:
      print("Directory does not exist")
      

