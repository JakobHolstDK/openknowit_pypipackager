from flask import Flask, render_template
from pymongo import MongoClient
import os


client = MongoClient(os.getenv("MONGO"))
db = client['pypi-packages']
pypipackages = db['pypi_packages']


app = Flask(__name__)


@app.route('/')
def index():
    data = pypipackages.find().__ordering__(('status', 'asc'))
    return render_template('main.html', data=data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)