from datetime import datetime
import json
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
from flask import current_app as app

# todo:- duration and actual end time

class SubTask(Resource):
    @f_jwt.jwt_required()
    def get(self, task_id):
        user_id = f_jwt.get_jwt_identity()
        # user_id=20
        app.logger.debug("user_id= %s", user_id)
        subtasks_list = []

        GET_SUBTASKS = '''SELECT id, title, description, status, plan_start_date, plan_end_date, 
        actual_end_date, duration, task_type, notify, repeat, priority 
        FROM subtasks WHERE user_id= %s and task_id= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_SUBTASKS, (user_id, task_id))
            rows = cursor.fetchall()
            if not rows:
                return {}
            for row in rows:
                subtask_dict = {}
                subtask_dict['id'] = row[0]
                subtask_dict['title'] = row[1]
                subtask_dict['description'] = row[2]
                subtask_dict['status'] = row[3]
                subtask_dict['plan_start_date'] = row[4]
                subtask_dict['plan_end_date'] = row[5]
                subtask_dict['actual_end_date'] = row[6]
                subtask_dict['duration'] = row[7]
                subtask_dict['task_type'] = row[8]
                subtask_dict['notify'] = row[9]
                subtask_dict['repeat'] = row[10]
                subtask_dict['priority'] = row[11]
                subtasks_list.append(subtask_dict)
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        app.logger.debug(subtasks_list)
        return subtasks_list

    @f_jwt.jwt_required()
    def post(self, task_id):
        user_id = f_jwt.get_jwt_identity()
        data = request.get_json()
        subtask_dict = json.loads(json.dumps(data))
        current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)
        CREATE_SUBTASK_RETURN_ID = '''INSERT INTO subtasks(user_id, task_id, title, description, status, 
        plan_start_date, plan_end_date, actual_end_date, duration, task_type, notify, repeat, priority, added_at) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(CREATE_SUBTASK_RETURN_ID,
                           (user_id, task_id, subtask_dict['title'], subtask_dict['description'], subtask_dict['status'],
                            subtask_dict['plan_start_date'], subtask_dict['plan_end_date'], subtask_dict['actual_end_date'],
                            subtask_dict['duration'], subtask_dict['task_type'], subtask_dict['notify'], subtask_dict['repeat'],
                            subtask_dict['priority'], current_time,))
            subtask_id = cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Subtask created with id = {subtask_id}."}, 201

    @f_jwt.jwt_required()
    def put(self, task_id, subtask_id):
        data = request.get_json()
        subtask_dict = json.loads(json.dumps(data))
        current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)
        
        UPDATE_SUBTASK = '''UPDATE subtasks SET title= %s, description= %s, status= %s,
        plan_start_date= %s, plan_end_date= %s, actual_end_date= %s, duration= %s, 
        task_type= %s, notify= %s, repeat= %s, priority= %s, updated_at= %s 
        WHERE id= %s AND task_id= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(UPDATE_SUBTASK, (subtask_dict['title'], subtask_dict['description'], subtask_dict['status'],
                            subtask_dict['plan_start_date'], subtask_dict['plan_end_date'], subtask_dict['actual_end_date'],
                            subtask_dict['duration'], subtask_dict['task_type'], subtask_dict['notify'], subtask_dict['repeat'],
                            subtask_dict['priority'], current_time, subtask_id, task_id,))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Subtask of id= {subtask_id} modified."}, 200

    @f_jwt.jwt_required()
    def delete(self, task_id, subtask_id):
        DELETE_SUBTASK = 'DELETE FROM subtasks WHERE id= %s AND task_id= %s'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(DELETE_SUBTASK, (subtask_id, task_id,))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return 200
