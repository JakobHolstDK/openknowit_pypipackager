from pymongo import MongoClient
import configparser
import re
import subprocess
import os
import requests
import sys
import toml 
from langchain.prompts import PromptTemplate
import json
from flask import Flask, request, jsonify


API_URL = os.getenv("PYPIAPI")
MONGO_URI = os.getenv("MONGO")
AITOKEN = os.getenv("OPENAI_API_KEY")

# Create a MongoDB client
client = MongoClient(MONGO_URI)
db = client['pypi-packages']


def registerpypipackage(name, version):
  package_data = {
            'name': name,
            'version': version,
            'status': "initial"
        }
  response = requests.post(API_URL, json=package_data)
  if response.status_code == 200:
    print(f'Registered package: {name}')
  else:
    print(f'Error registering package {name}: {response.text}')

def updatepypipackage(name, version, status):
  package_data = {
            'name': name,
            'version': version,
            'status': status
        }
  response = requests.post(API_URL, json=package_data)
  if response.status_code == 200:
    print(f'Updated package: {name}')
  else:
    print(f'Error updating package {name}: {response.text}')
   

def filenames(mypath):
  file_names = []
  files = os.listdir(mypath)
  for file in files:
    file_names.append(file)
  return file_names

def diflist(list1 , list2):
  list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
  return list_dif

def downloadpypipackage(name, version):
  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  package_name = name + '==' + version
  #subprocess.call(["pip", "download", "-d", download_folder, package_name])
  before = filenames(download_folder)
  subprocess.call(["pip", "download", '--no-binary' , ':all:',  "-d", download_folder, package_name])
  after = filenames(download_folder)
  diff = diflist(before, after)
  downloads = []
  for i in diff:
    newpackage = i[::-1].split('-', 1)[1][::-1]
    newversion = i[::-1].split('-', 1)[0][::-1].replace('.tar.gz', '').replace('.whl', '').replace('.zip', '')
    downloads.append({'filename': i, 'package': newpackage, 'version': newversion})
  return downloads

  

query = {'sourcedownloaded': False}
packages = db['pypi_packages']
for package in packages.find(query):
    downloads = downloadpypipackage(package['name'], package['version'])
    for download in downloads:
      query = {'name': package['name'], 'version': package['version']}
      update = {'$push': {'downloads': download}}
      packages.update_one(query, update)
    query = {'name': package['name'], 'version': package['version']}
    update = {'$set': {'sourcedownloaded': True}}
    packages.update_one(query, update)
    print(f"Downloaded source for {package['name']} {package['version']}")

    


