import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)

# gets variables from environment
db_url = os.getenv("DATABASE_URL")
if db_url == None:
    db_url = os.getenv("LOCAL_DATABASE_URL", "Not found")
app.logger.debug('db_url=%s ', db_url)

db_conn = psycopg2.connect(db_url)


@app.get("/")  # http://127.0.0.1:5000/
def get_index():
    return "Welcome to task tracker app!!!"


if __name__ == "__main__":
    app.run()
