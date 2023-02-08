import psycopg2
from flask import Flask, request
from flask_restful import Api
import flask_jwt_extended

# local imports
from app.config import app_config
from app.resources.auth import Register, Login, RefreshToken
from app.resources.user import UserProfile, ResetEmail, ResetPhone, ResetPassword
from app.resources.list import List
from app.resources.event import Event
from app.resources.task import Task
from app.resources.subtask import SubTask
from app.resources.basket import Basket
from app.resources.home import MyDayTask, PlannedTask
from app.resources.assign import Assignment
from app.resources.setting import UserSetting

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

    # todo
    api.add_resource(ResetEmail, '/reset-email')
    api.add_resource(ResetPhone, '/reset-phone')
    api.add_resource(ResetPassword, '/reset-password')

    api.add_resource(List, '/lists', '/lists/<int:list_id>')


    api.add_resource(Task, '/tasks', '/tasks/<int:task_id>')
    api.add_resource(SubTask, '/tasks/<int:task_id>/subtasks',
                     '/tasks/<int:task_id>/subtasks/<int:subtask_id>')

    # Home
    api.add_resource(MyDayTask, '/my-day')
    api.add_resource(PlannedTask, '/planned')

    api.add_resource(Event, '/events', '/events/<int:event_id>')

    api.add_resource(Basket, '/baskets', '/baskets/<int:basket_id>')

    api.add_resource(Assignment, '/assigns', '/assigns/<int:task_id>')

    api.add_resource(UserSetting, '/users/settings', '/users/settings/<int:setting_id>')

    return app
