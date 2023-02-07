from datetime import datetime
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
from flask import current_app as app


class Event(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
        app.logger.debug("user_id= %s", user_id)
        events_list = []

        args = request.args  # retrieve args from query string
        event_type_arg = args.get('type', None)
        event_date_arg = args.get('date', None)
        app.logger.debug("?type=%s&date=%s", event_type_arg, event_date_arg)

        if event_type_arg == None and event_date_arg == None:
            GET_EVENTS = '''SELECT id, name, event_type, TO_CHAR(event_date, 'YYYY-MM-DD'),
            TO_CHAR(event_end_date, 'YYYY-MM-DD'), notify, repeat FROM events WHERE user_id= %s'''
            GET_EVENTS_TUPLE = (user_id,)
        elif event_type_arg != None and event_date_arg == None:
            GET_EVENTS = '''SELECT id, name, event_type, TO_CHAR(event_date, 'YYYY-MM-DD'),
            TO_CHAR(event_end_date, 'YYYY-MM-DD'), notify, repeat FROM events WHERE user_id= %s
            AND event_type= %s'''
            GET_EVENTS_TUPLE = (user_id, event_type_arg,)
        elif event_type_arg == None and event_date_arg != None:
            GET_EVENTS = '''SELECT id, name, event_type, TO_CHAR(event_date, 'YYYY-MM-DD'),
            TO_CHAR(event_end_date, 'YYYY-MM-DD'), notify, repeat FROM events WHERE user_id= %s
            AND event_date= %s'''
            GET_EVENTS_TUPLE = (user_id, event_date_arg,)
        elif event_type_arg != None and event_date_arg != None:
            GET_EVENTS = '''SELECT id, name, event_type, TO_CHAR(event_date, 'YYYY-MM-DD'),
            TO_CHAR(event_end_date, 'YYYY-MM-DD'), notify, repeat FROM events WHERE user_id= %s
            AND event_type= %s AND event_date= %s'''
            GET_EVENTS_TUPLE = (user_id, event_type_arg, event_date_arg,)

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_EVENTS, GET_EVENTS_TUPLE)
            rows = cursor.fetchall()
            if not rows:
                return {}
            for row in rows:
                event_dict = {}
                event_dict['id'] = row[0]
                event_dict['name'] = row[1]
                event_dict['event_type'] = row[2]
                event_dict['event_date'] = row[3]
                event_dict['event_end_date'] = row[4]
                event_dict['notify'] = row[5]
                event_dict['repeat'] = row[6]
                events_list.append(event_dict)
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        app.logger.debug(events_list)
        return events_list

    @f_jwt.jwt_required()
    def post(self):
        user_id = f_jwt.get_jwt_identity()
        data = request.get_json()
        name = data["name"]
        event_type = data["event_type"]
        event_date = data["event_date"]
        event_end_date = data["event_end_date"]
        notify = data["notify"]
        repeat = data["repeat"]
        current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)
        CREATE_EVENT_RETURN_ID = '''INSERT INTO events(user_id, name, event_type,
         event_date, event_end_date, notify, repeat, added_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(CREATE_EVENT_RETURN_ID,
                           (user_id, name, event_type, event_date, event_end_date, notify, repeat, current_time,))
            event_id = cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Event {name} created with id = {event_id}."}, 201

    @f_jwt.jwt_required()
    def put(self, event_id):
        data = request.get_json()
        name = data["name"]
        event_type = data["event_type"]
        event_date = data["event_date"]
        event_end_date = data["event_end_date"]
        notify = data["notify"]
        repeat = data["repeat"]
        current_time = datetime.now()

        UPDATE_EVENT = '''UPDATE events SET name= %s, event_type= %s, event_date= %s, event_end_date= %s, 
        notify= %s, repeat= %s, updated_at= %s where id = %s'''

        try:
            cursor = main.db_conn.cursor()
            cursor.execute(UPDATE_EVENT, (name, event_type, event_date,
                           event_end_date, notify, repeat, current_time, event_id))

        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')

        finally:
            cursor.close()
        return {"message": f"Event {name} created with id = {event_id}."}, 200

    @f_jwt.jwt_required()
    def delete(self, event_id):
        DELETE_EVENT = 'DELETE FROM events WHERE id= %s'

        try:
            cursor = main.db_conn.cursor()
            cursor.execute(DELETE_EVENT, (event_id,))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return 200
