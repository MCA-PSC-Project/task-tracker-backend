from datetime import datetime
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
from flask import current_app as app


class List(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
        # user_id=20
        app.logger.debug("user_id= %s", user_id)
        lists_list = []

        GET_LISTS = 'SELECT id, name FROM lists WHERE user_id= %s'
        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_LISTS, (user_id,))
            rows = cursor.fetchall()
            if not rows:
                return {}
            for row in rows:
                list_dict={}
                list_dict['id'] = row[0]
                list_dict['name'] = row[1]
                lists_list.append(list_dict)
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        app.logger.debug(lists_list)
        return lists_list

    @f_jwt.jwt_required()
    def post(self):
        user_id = f_jwt.get_jwt_identity()
        data = request.get_json()
        name = data["name"]
        current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)
        CREATE_LIST_RETURN_ID = 'INSERT INTO lists(user_id, name, added_at) VALUES(%s, %s, %s) RETURNING id'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(CREATE_LIST_RETURN_ID,
                           (user_id, name, current_time,))
            list_id = cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"List {name} created with id = {list_id}."}, 201

    @f_jwt.jwt_required()
    def put(self, list_id):
        data = request.get_json()
        name = data["name"]
        current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)
        UPDATE_LIST = 'UPDATE lists SET name= %s, updated_at= %s WHERE id= %s'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(UPDATE_LIST, (name, current_time, list_id,))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"List {name} modified."}, 200

    @f_jwt.jwt_required()
    def delete(self, list_id):
        DELETE_LIST = 'DELETE FROM lists WHERE id= %s'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(DELETE_LIST, (list_id,))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return 200
