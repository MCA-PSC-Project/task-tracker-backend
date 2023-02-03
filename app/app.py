import os
import psycopg2
from flask import Flask, request
from flask_restful import Api

# local imports
from app.config import app_config
from app.resources.user import User


# db_conn = psycopg2.connect()
# app.logger.debug('DATABASE_URI=%s ', app_configDATABASE_URI)


# @app.get("/")  # http://127.0.0.1:5000/
# def get_index():
#     return "Welcome to task tracker app!!!"


def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.logger.debug(app_config[config_name])
    app.logger.debug('DATABASE_URI=%s ' % app.config['DATABASE_URI'])
    app.logger.debug('SECRET=%s ' % app.config['SECRET'])

    db_conn = psycopg2.connect(app.config['DATABASE_URI'])


    # api.add_resource(User, '/users', '/users/<string:id>')
    api.add_resource(User, '/users/profile')

    return app
