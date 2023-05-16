from flask import Flask, render_template
from pymongo import MongoClient
import os


client = MongoClient(os.getenv("MONGO"))
db = client['pypi-packages']
pypipackages = db['pypi_packages']


app = Flask(__name__)


@app.route('/')
def index():
    data = pypipackages.find()
    return render_template('main.html', data=sorted_data(data))

def sort_data(data):
    # Sort the data based on priority
    sorted_data = sorted(data, key=lambda x: (x['status'], x['version']))
    
    return sorted_data
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)