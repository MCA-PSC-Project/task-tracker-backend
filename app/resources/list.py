from datetime import datetime
from flask import request
from flask_restful import Resource
from psycopg2 import Error as pg_error
import app.db as db


class List(Resource):
    def get(self):
        return {"user": "prashant"}

    def post(self):
        data = request.get_json()
        name = data["name"]
        user_id = None
        current_time = datetime.now()
        print("cur time :", current_time)
        CREATE_LIST_RETURN_ID = 'INSERT INTO lists(user_id, name, added_at) VALUES(%s, %s, %s)'

        # declare a cursor object from the connection
        cursor = db.db_conn.cursor()
        print("cursor object:", cursor, "\n")

        # catch exception for invalid SQL statement
        try:
            # cursor.execute("INVALID SQL STATEMENT")
            cursor.execute(CREATE_LIST_RETURN_ID,
                           (user_id, name, current_time))
            # list_id = cursor.fetch_one()[0]
        except (Exception, pg_error) as err:
            # pass exception to function
            # db.print_psycopg2_exception(err)
            print(err)
            return
        finally:
            cursor.close()
        return {"message": f"List {name} created."}, 201

    def put(self):
        pass

    def delete(self):
        pass
