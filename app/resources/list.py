from datetime import datetime
from flask import request
from flask_restful import Resource

import app.db as db


class List(Resource):
    def get(self):
        return {"user": "prashant"}

    def post(self):
        data = request.get_json()
        name = data["name"]
        user_id = None
        current_time = datetime.now()
        CREATE_LIST_RETURN_ID = 'INSERT INTO lists(user_id, name, added_at) VALUES(%s, %s, %s)'
        with db.db_conn.cursor() as cursor:
            cursor.execute(CREATE_LIST_RETURN_ID,
                           (user_id, name, current_time))
            # list_id = cursor.fetch_one()[0]
        return { "message": f"List {name} created."}, 201

    def put(self):
        pass

    def delete(self):
        pass
