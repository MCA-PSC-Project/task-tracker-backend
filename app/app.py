import psycopg2
from flask import Flask, request
from flask_restful import Api
import flask_jwt_extended

# local imports
from app.config import app_config
from app.resources.auth import Register, Login, RefreshToken
from app.resources.user import UserProfile, ResetEmail, ResetPhone, ResetPassword
from app.resources.list import List

import app.main as main

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
    app.logger.debug('JWT_SECRET_KEY=%s ' % app.config['JWT_SECRET_KEY'])

    # global db_conn
    main.db_conn = psycopg2.connect(app.config['DATABASE_URI'])

    if main.db_conn == None:
        app.logger.fatal('Database connection error')
    main.db_conn.autocommit = True

    main.jwt = flask_jwt_extended.JWTManager(app)

    api.add_resource(Register, '/auth/register')
    api.add_resource(Login, '/auth/login')
    api.add_resource(RefreshToken, '/auth/refresh')

    api.add_resource(UserProfile, '/users/profile')

    #todo
    api.add_resource(ResetEmail, '/reset-email')
    api.add_resource(ResetPhone, '/reset-phone')
    api.add_resource(ResetPassword, '/reset-password')

    api.add_resource(List, '/lists', '/lists/<int:list_id>')

    return app
