from datetime import datetime
import json
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
from flask import current_app as app

# todo:- duration and actual end time


class MyDayTask(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
        task_type = 'my_day'
        # user_id=20
        app.logger.debug("user_id= %s", user_id)
        tasks_list = []

        GET_MY_DAY_TASKS = '''SELECT id, title, description, status, TO_CHAR(plan_start_date, 'YYYY-MM-DD'), 
        TO_CHAR(plan_end_date, 'YYYY-MM-DD'), TO_CHAR(actual_end_date, 'YYYY-MM-DD'), duration, 
        task_type, notify, repeat, priority 
        FROM tasks WHERE user_id= %s AND task_type= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_MY_DAY_TASKS, (user_id, task_type,))
            rows = cursor.fetchall()
            if not rows:
                return {}
            for row in rows:
                task_dict = {}
                task_dict['id'] = row[0]
                task_dict['title'] = row[1]
                task_dict['description'] = row[2]
                task_dict['status'] = row[3]
                task_dict['plan_start_date'] = row[4]
                task_dict['plan_end_date'] = row[5]
                task_dict['actual_end_date'] = row[6]
                task_dict['duration'] = row[7]
                task_dict['task_type'] = row[8]
                task_dict['notify'] = row[9]
                task_dict['repeat'] = row[10]
                task_dict['priority'] = row[11]
                tasks_list.append(task_dict)
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        app.logger.debug(tasks_list)
        return tasks_list

class PlannedTask(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
        task_type = 'planned'
        # user_id=20
        app.logger.debug("user_id= %s", user_id)
        tasks_list = []

        GET_MY_DAY_TASKS = '''SELECT id, title, description, status, TO_CHAR(plan_start_date, 'YYYY-MM-DD'), 
        TO_CHAR(plan_end_date, 'YYYY-MM-DD'), TO_CHAR(actual_end_date, 'YYYY-MM-DD'), duration, 
        task_type, notify, repeat, priority 
        FROM tasks WHERE user_id= %s AND task_type= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_MY_DAY_TASKS, (user_id, task_type,))
            rows = cursor.fetchall()
            if not rows:
                return {}
            for row in rows:
                task_dict = {}
                task_dict['id'] = row[0]
                task_dict['title'] = row[1]
                task_dict['description'] = row[2]
                task_dict['status'] = row[3]
                task_dict['plan_start_date'] = row[4]
                task_dict['plan_end_date'] = row[5]
                task_dict['actual_end_date'] = row[6]
                task_dict['duration'] = row[7]
                task_dict['task_type'] = row[8]
                task_dict['notify'] = row[9]
                task_dict['repeat'] = row[10]
                task_dict['priority'] = row[11]
                tasks_list.append(task_dict)
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        app.logger.debug(tasks_list)
        return tasks_list

