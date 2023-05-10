from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

@app.route('/pypi-packages', methods=['POST'])
def register_pypi_package():
    package_data = request.get_json()
    pypi_packages = db['pypi_packages']
    pypi_packages.insert_one(package_data)
    return jsonify({'success': True, 'message': 'PyPI package registered successfully'})

if __name__ == '__main__':
    app.run()
