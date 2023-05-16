from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = [...]  # Replace [...] with the actual data list
    return render_template('main.html', data=data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)