from datetime import datetime
import json
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
from flask import current_app as app


class Assignment(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
        app.logger.debug("user_id= %s", user_id)
        tasks_list = []

        args = request.args  # retrieve args from query string
        to_arg = args.get('to', None)
        app.logger.debug("?to=%s", to_arg)

        if to_arg == None:
            abort(400, 'Bad Request')
        elif to_arg == 'others':
            GET_ASSIGNED_TASKS = '''SELECT t.id, t.title, t.description, t.status, TO_CHAR(t.plan_start_date, 'YYYY-MM-DD'), 
            TO_CHAR(t.plan_end_date, 'YYYY-MM-DD'), TO_CHAR(t.actual_end_date, 'YYYY-MM-DD'), 
            t.duration, t.task_type, t.notify, t.repeat, t.priority, 
            (SELECT email FROM users WHERE id = at.assignee_user_id), TO_CHAR(at.assigned_at, 'YYYY-MM-DD'), at.status 
            FROM tasks t JOIN assigned_tasks at ON t.id = at.task_id
            WHERE at.assigner_user_id= %s'''
        elif to_arg == 'me':
            GET_ASSIGNED_TASKS = '''SELECT t.id, t.title, t.description, t.status, TO_CHAR(t.plan_start_date, 'YYYY-MM-DD'), 
            TO_CHAR(t.plan_end_date, 'YYYY-MM-DD'), TO_CHAR(t.actual_end_date, 'YYYY-MM-DD'), 
            t.duration, t.task_type, t.notify, t.repeat, t.priority, 
            (SELECT email FROM users WHERE id = at.assigner_user_id), TO_CHAR(at.assigned_at, 'YYYY-MM-DD'), at.status 
            FROM tasks t JOIN assigned_tasks at ON t.id = at.task_id
            WHERE at.assignee_user_id= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_ASSIGNED_TASKS, (user_id, ))
            rows = cursor.fetchall()
            if not rows:
                return {}

            if to_arg == 'others':
                id_key = 'asssignee_email'
            elif to_arg == 'me':
                id_key = 'asssigner_email'

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

                task_dict[id_key] = row[12]

                task_dict['assigned_at'] = row[13]
                task_dict['status'] = row[14]
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
        assign_task_dict = json.loads(json.dumps(data))
        current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)

        # Get assignee user id from provided assignee email
        GET_ID_FROM_EMAIL = 'SELECT id FROM users WHERE email= %s'
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_ID_FROM_EMAIL,
                           (assign_task_dict.get('assignee_email'),))
            row = cursor.fetchone()
            if row is None:
                abort(400, 'Bad Request : Email not found')
            else:
                assignee_user_id = row[0]
                app.logger.debug("assignee_user_id= %s", assignee_user_id)
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()

        ASSIGN_TASK = '''INSERT INTO assigned_tasks(assigner_user_id, assignee_user_id, task_id, assigned_at) 
        VALUES(%s, %s, %s, %s)'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(ASSIGN_TASK, (user_id, assignee_user_id,
                           assign_task_dict['task_id'], current_time))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Task assigned to user with email= {assign_task_dict.get('assignee_email')}"}, 201

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
