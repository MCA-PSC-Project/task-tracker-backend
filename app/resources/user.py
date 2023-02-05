from datetime import datetime
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
import json


class UserProfile(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
        # user_id=20
        print("user_id=", user_id)
        user_profile_dict = {}

        GET_PROFILE = '''SELECT name, email, phone, TO_CHAR(dob, 'YYYY-MM-DD'), gender FROM users WHERE id= %s'''
        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            print("cursor object:", cursor, "\n")

            cursor.execute(GET_PROFILE, (user_id,))
            rows = cursor.fetchall()
            if not rows:
                return {}
            for row in rows:
                user_profile_dict['name'] = row[0]
                user_profile_dict['email'] = row[1]
                user_profile_dict['phone'] = row[2]
                user_profile_dict['dob'] = row[3]
                user_profile_dict['gender'] = row[4]
        except (Exception, psycopg2.Error) as err:
            print(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        print(user_profile_dict)
        return user_profile_dict

    @f_jwt.jwt_required()
    def put(self):
        user_id = f_jwt.get_jwt_identity()
        # user_id=20
        print("user_id=", user_id)
        data = request.get_json()
        user_dict = json.loads(json.dumps(data))
        print(user_dict)

        current_time = datetime.now()
        # print("cur time :", current_time)
        UPDATE_USER = 'UPDATE users SET name= %s, dob=%s, gender=%s, updated_at= %s WHERE id= %s'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            print("cursor object:", cursor, "\n")

            cursor.execute(
                UPDATE_USER, (user_dict['name'], user_dict['dob'], user_dict['gender'], current_time, user_id,))
        except (Exception, psycopg2.Error) as err:
            print(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"user {user_dict['name']} modified."}, 200

    @f_jwt.jwt_required()
    def delete(self):
        user_id = f_jwt.get_jwt_identity()
        # user_id=20
        print("user_id=", user_id)

        current_time = datetime.now()
        # print("cur time :", current_time)
        DELETE_USER = 'DELETE FROM users WHERE id= %s'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            print("cursor object:", cursor, "\n")

            cursor.execute(DELETE_USER, (user_id,))
        except (Exception, psycopg2.Error) as err:
            print(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return 200
