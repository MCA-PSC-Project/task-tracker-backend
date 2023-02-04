import os
import psycopg2
from flask import Flask, request
from flask_restful import Api

# local imports
from app.config import app_config
from app.resources.user import User
from app.resources.list import List

import app.db as db

# db_conn = psycopg2.connect()
# app.logger.debug('DATABASE_URI=%s ', app_configDATABASE_URI)


# @app.get("/")  # http://127.0.0.1:5000/
# def get_index():
#     return "Welcome to task tracker app!!!"

# db_conn=None

def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.logger.debug(app_config[config_name])
    app.logger.debug('DATABASE_URI=%s ' % app.config['DATABASE_URI'])
    app.logger.debug('SECRET=%s ' % app.config['SECRET'])

    # global db_conn
    db.db_conn = psycopg2.connect(app.config['DATABASE_URI'])

    if db.db_conn == None:
        app.logger.fatal('Database connection error')

    db.db_conn.autocommit = True
    # api.add_resource(User, '/users', '/users/<string:id>')
    # api.add_resource(User, '/users/profile')
    api.add_resource(List, '/lists', '/lists/<int:list_id>')

    return app
