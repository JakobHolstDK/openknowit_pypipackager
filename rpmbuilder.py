from pymongo import MongoClient
import subprocess
import os
import sys



# Create a MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['pypi-packages']

def unpack_whl_file(filename):
  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  subprocess.call(["cd", download_folder, "&&" "wheel", "unpack", filename])

def downloadpypipackage(name, version):
  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  package_name = name + '==' + version
  subprocess.call(["pip", "download", "-d", download_folder, package_name])
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
    print(package['name'])
    print(package['version'])
    print(package['rpmbuild'])
    filename = downloadpypipackage(package['name'], package['version'])
    print(filename)
    query = {'name': package['name'], 'version': package['version']}
    update = {'$set': {'sourcefile': filename}}
    packages.update_one(query, update)
    print(unpack_whl_file(filename))




    


