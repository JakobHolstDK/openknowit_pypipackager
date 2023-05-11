from pymongo import MongoClient
import configparser
import subprocess
import os
import requests
import sys
import toml 
from langchain.prompts import PromptTemplate
import json

API_URL = os.getenv("PYPIAPI")
MONGO_URI = os.getenv("MONGO")
AITOKEN = os.getenv("OPENAI_API_KEY")



# Create a MongoDB client
client = MongoClient(MONGO_URI)
db = client['pypi-packages']

def createsetuppyfrompyprojecttoml(name, version):
  print("Creating setup.py file from pyproject.toml file")
  print("This is a temporary solution, please add a setup.py file to your project"
        "and upload it to your repository")
  print("This will be fixed in the future")
  print("the name is: " + name + " and the version is: " + version)

  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  source_folder = download_folder + name + '-' + version
  pyprojecttoml_file = source_folder + '/' + 'pyproject.toml'
  setuppy_file = source_folder + '/' + 'setup.py'
  if os.path.exists(pyprojecttoml_file):
    with open(pyprojecttoml_file, "r") as f:
      config = toml.load(f)
    try: 
      if config["tool"]["poetry"]["name"] == name:
        poetry = True
    except:
        poetry = False

    if  poetry:
      print("The name in the pyproject.toml has a poetry entry with the same name as the package")
      project_name = config["tool"]["poetry"]["name"]
      project_version = config["tool"]["poetry"]["version"]
      project_description = config["tool"]["poetry"]["description"]
      project_license = config["tool"]["poetry"]["license"]
      project_url = config["tool"]["poetry"]["homepage"]
      project_authors = config["tool"]["poetry"]["authors"]
    
      
    try: 
      if config['project']['name'] == name:
        project = True
    except:
        project = False

    if  project:
        print("The name in the pyproject.toml has a project entry with the same name as the package")
        project_name = config['project']['name']
        if 'version' in config['project']:
          project_version = config['project']['version']
        else:
          project_version = version
        if 'description' in config['project']:

          project_description = config['project']['description']
        else:
          project_description = ''

        if 'license' in config['project']:
          project_license = config['project']['license']
        else:
          project_license = ''

        if 'project_url' in config['project']:
           project_url = config['project']['project_url']
        else:
           project_url = ''

        if 'project_authors' in config['project']:
          project_authors = config['project']['project_authors']
        else:
          project_authors = ''

           

        project_authors = config['project']['authors']

    if not project and not poetry:
      print("The name in the pyproject.toml has no project or poetry entry with the same name as the package")
      print("Please add a setup.py file to your project and upload it to your repository")
      print("This will be fixed in the future")
      sys.exit(1)   

    # Generate the setup.py file
    with open(setuppy_file, "w") as f:
      f.write(f"""
    from setuptools import setup, find_packages
    setup(
      name="{project_name}",
      version="{project_version}",
      description="{project_description}",
      license="{project_license}",
      url="{project_url}",
      author="{project_authors}",
      packages=find_packages(),
    )
    """
              )
def replace_setupcfg_with_pyprojecttoml(setupcfg_file, pyprojecttoml_file):
# Read the contents of setup.cfg
  config = configparser.ConfigParser()
  config.read(setupcfg_file)

# Extract the relevant fields from setup.cfg
  name = config["metadata"]["name"]
  version = config["metadata"]["version"]
  description = config["metadata"]["description"]
  url = config["metadata"]["url"]
  author = config["metadata"]["author"]
  author_email = config["metadata"]["author_email"]
  license = config["metadata"]["license"]
  classifiers = config["metadata"]["classifiers"].split("\n")
  requires_python = config["metadata"]["requires_python"]
  # Load the existing pyproject.toml file
  with open(pyprojecttoml_file, "r") as f:
    pyproject = toml.load(f)

  # Construct the pyproject.toml file
  # Merge the new fields with the existing pyproject.toml file
  poetry = pyproject["tool"]["poetry"]
  poetry["name"] = name
  poetry["version"] = version
  poetry["description"] = description
  poetry["homepage"] = url
  poetry["authors"] = [f"{author} <{author_email}>"]
  poetry["license"] = license
  poetry["classifiers"] = classifiers

  # Write the updated pyproject.toml file
  with open(pyprojecttoml_file, "w") as f:
    toml.dump(pyproject, f)


def prettymysetuppy(name, version):
  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  source_folder = download_folder + name + '-' + version
  setuppy_file = source_folder + '/' + 'setup.py'
  setupcfg_file = source_folder + '/' + 'setup.cfg'
  prettysetuppy_file = source_folder + '/' + 'pretty.setup.py'
  pyprojecttoml_file = source_folder + '/' + 'pyproject.toml'
  if os.path.exists(setupcfg_file):
     checksetupcfg = open(setupcfg_file, 'r').read()
     if 'name' in checksetupcfg:
        replace_setupcfg_with_pyprojecttoml(setupcfg_file, pyprojecttoml_file)
        os.remove(setupcfg_file)
        os.remove(setuppy_file)

  if not os.path.exists(setuppy_file):
     if os.path.exists(pyprojecttoml_file):
       createsetuppyfrompyprojecttoml(name, version)
     
  setupfile = ""
  if os.path.exists(setuppy_file):
    with open(setuppy_file, 'r') as file:
      data = file.readlines()
      for line in data:
        setupfile += line
    prompt = PromptTemplate(
      input_variables=["setupfile"],
      template="Pretty this python setup-py file. the file has to have : {setupfile}",
    )
    response = prompt.format(setupfile=setupfile)
    response = response.replace("Pretty this python setup-py file : ", "")

    open(prettysetuppy_file, 'w').write(response)


  


  
      
   

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

def create_spec_file(name, version):
  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  source_folder = download_folder + name + '-' + version
  spec_file = source_folder + '/' + name + '.spec'

  subprocess.call(["tar", "-xzf", download_folder + filename, '-C' , download_folder])


def unpack_gz_file(filename):
  download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
  subprocess.call(["tar", "-xzf", download_folder + filename, '-C' , download_folder])

def unpack_zip_file(filename):
   download_folder = os.getenv('DOWNLOAD_FOLDER', '/tmp')
   print("HELLLLLP")


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



query = {'rpmbuild': False}
packages = db['pypi_packages']
for package in packages.find(query):
    prettymysetuppy(package['name'],  package['version'])




    


