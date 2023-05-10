from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util
import json


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['pypi-packages']
#pypipackager = db['pypi_packages']
#pypipackager.delete_many({})



@app.route('/pypi-packages', methods=['POST'])
def register_pypi_package():
    package_data = request.get_json()
    pypi_packages = db['pypi_packages']
    query = {'name': package_data['name'], 'version': package_data['version']}
    if pypi_packages.find_one(query):
        return jsonify({'success': False, 'message': 'PyPI package already registered'})    
    else:
        pypi_packages.insert_one(package_data)
        return jsonify({'success': True, 'message': 'PyPI package registered successfully'})

@app.route('/pypi-packages', methods=['GET'])
def get_pypi_packages():
    pypi_packages = db['pypi_packages']
    return json.loads(json_util.dumps(pypi_packages.find()))

if __name__ == '__main__':
    app.run()
