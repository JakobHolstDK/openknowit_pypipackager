from pymongo import MongoClient
import subprocess
import os
import requests
import sys
API_URL = 'http://localhost:5000/pypi-packages'


# Create a MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['pypi-packages']
def registerpypipackage(name, version):
  package_data = {
            'name': name,
            'version': version,
            'rpmbuild': False,
            'debbuild': False
        }
  response = requests.post(API_URL, json=package_data)
  if response.status_code == 200:
    print(f'Registered package: {name}')
  else:
    print(f'Error registering package {name}: {response.text}')

def filenames(mypath):
  file_names = []
  files = os.listdir(mypath)
  for file in files:
    file_names.append(file)
  return file_names

def diflist(list1 , list2):
  list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
  return list_dif
    
def unpack_whl_file(filename):
  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  subprocess.call(["wheel", "unpack", filename, '--dest' , download_folder])

def downloadpypipackage(name, version):
  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  package_name = name + '==' + version
  #subprocess.call(["pip", "download", "-d", download_folder, package_name])
  before = filenames(download_folder)
  subprocess.call(["pip", "download", '--no-binary' , ':all:',  "-d", download_folder, package_name])
  after = filenames(download_folder)
  diff = diflist(before, after)
  for i in diff:

    newpackage = i[::-1].split('-', 1)[1][::-1]
    newversion = i[::-1].split('-', 1)[0][::-1].replace('.tar.gz', '').replace('.whl', '').replace('.zip', '')

    print(newpackage)
    print(newversion)
  print(diff)

  #pip download --no-binary :all: -d /path/to/directory requests

  for filename in os.listdir(download_folder):
        if filename.startswith(name + '-') and filename.endswith('.whl'):
            return os.path.join(download_folder, filename)
  for filename in os.listdir(download_folder):
        name = name.replace('-','_')
        if filename.startswith(name + '-') and filename.endswith('.whl'):
            return os.path.join(download_folder, filename)
  return None




query = {'rpmbuild': False}
packages = db['pypi_packages']
for package in packages.find(query):
    filename = downloadpypipackage(package['name'], package['version'])
    query = {'name': package['name'], 'version': package['version']}
    update = {'$set': {'sourcefile': filename}}
    packages.update_one(query, update)

download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
for file in filenames(download_folder):
  if file.endswith('.gz'):  
    unpack_gz_file(file)
  if file.endswith('.zip'):
    unpack_zip_file(file)

     os.remove(files)





    


