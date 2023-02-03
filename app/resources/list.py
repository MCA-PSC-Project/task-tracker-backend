from datetime import datetime
from flask import request
from flask_restful import Resource

# from .../app import db_conn


class List(Resource):
    def get(self):
        return {"user": "prashant"}

    def post(self):
        data = request.get_json()
        name = data["name"]
        user_id = None
        current_time = datetime.now()
        CREATE_LIST_RETURN_ID = 'INSERT INTO lists(user_id, name, added_at) VALUES(%s, %s, %s)'
        with db_conn.cursor() as cursor:
            cursor.execute(CREATE_LIST_RETURN_ID,
                           (user_id, name, current_time))
            list_id = cursor.fetchone()[0]
        return {"id": list_id, "message": f"List {name} created."}, 201

    def put(self):
        pass

    def delete(self):
        pass
