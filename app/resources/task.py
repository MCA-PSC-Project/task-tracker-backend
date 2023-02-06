from datetime import datetime
import json
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
from flask import current_app as app


class Task(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
        # user_id=20
        app.logger.debug("user_id= %s", user_id)
        tasks_list = []

        GET_TASKS = '''SELECT id, title, description, status, plan_start_date, plan_end_date, 
        actual_end_date, duration, task_type, notify, repeat, priority 
        FROM tasks WHERE user_id= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_TASKS, (user_id,))
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

    @f_jwt.jwt_required()
    def post(self):
        user_id = f_jwt.get_jwt_identity()
        data = request.get_json()
        task_dict = json.loads(json.dumps(data))
        current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)
        CREATE_TASK_RETURN_ID = '''INSERT INTO tasks(user_id, title, description, status, plan_start_date, plan_end_date, 
        actual_end_date, duration, task_type, notify, repeat, priority, added_at) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(CREATE_TASK_RETURN_ID,
                           (user_id, task_dict['title'], task_dict['description'], task_dict['status'],
                            task_dict['plan_start_date'], task_dict['plan_end_date'], task_dict['actual_end_date'],
                            task_dict['duration'], task_dict['task_type'], task_dict['notify'], task_dict['repeat'],
                            task_dict['priority'], current_time,))
            task_id = cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Task created with id = {task_id}."}, 201

    @f_jwt.jwt_required()
    def put(self, task_id):
        data = request.get_json()
        task_dict = json.loads(json.dumps(data))
        current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)
        
        UPDATE_TASK = '''UPDATE tasks SET title= %s, description= %s, status= %s,
        plan_start_date= %s, plan_end_date= %s, actual_end_date= %s, duration= %s, 
        task_type= %s, notify= %s, repeat= %s, priority= %s, updated_at= %s 
        WHERE id=%s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(UPDATE_TASK, (task_dict['title'], task_dict['description'], task_dict['status'],
                            task_dict['plan_start_date'], task_dict['plan_end_date'], task_dict['actual_end_date'],
                            task_dict['duration'], task_dict['task_type'], task_dict['notify'], task_dict['repeat'],
                            task_dict['priority'], current_time, task_id))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Task of id= {task_id} modified."}, 200

    @f_jwt.jwt_required()
    def delete(self, task_id):
        DELETE_TASK = 'DELETE FROM tasks WHERE id= %s'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(DELETE_TASK, (task_id,))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return 200
