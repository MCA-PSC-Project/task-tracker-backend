from flask import Flask

app = Flask(__name__)


@app.get("/")  # http://127.0.0.1:5000/
def get_stores():
    return "Welcome to task tracker app!!!"
