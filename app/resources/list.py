from datetime import datetime
from flask import request
from flask_restful import Resource
import psycopg2
import app.db as db


class List(Resource):
    def get(self):
        user_id = 19
        lists_dict = {}
        
        GET_LISTS = 'SELECT id, name FROM lists WHERE id= %s'
        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = db.db_conn.cursor()
            print("cursor object:", cursor, "\n")

            cursor.execute(GET_LISTS, (user_id,))
            rows = cursor.fetchall()
            if not rows:
                return {}
            for row in rows:
                lists_dict['id'] = row[0]
                lists_dict['name'] = row[1]
        except (Exception, psycopg2.Error) as err:
            print(err)
            return
        finally:
            cursor.close()
        print(lists_dict)
        return lists_dict

    def post(self):
        data = request.get_json()
        name = data["name"]
        user_id = None
        current_time = datetime.now()
        print("cur time :", current_time)
        CREATE_LIST_RETURN_ID = 'INSERT INTO lists(user_id, name, added_at) VALUES(%s, %s, %s) RETURNING id'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = db.db_conn.cursor()
            print("cursor object:", cursor, "\n")

            cursor.execute(CREATE_LIST_RETURN_ID,
                           (user_id, name, current_time,))
            list_id = cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as err:
            print(err)
            return
        finally:
            cursor.close()
        return {"message": f"List {name} created with id = {list_id}."}, 201

    def put(self):
        pass

    def delete(self):
        pass
