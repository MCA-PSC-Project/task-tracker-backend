from datetime import datetime, timedelta, timezone
from flask import request, abort, jsonify
from flask_restful import Resource
import flask_jwt_extended as f_jwt
import psycopg2
import app.main as main
import bcrypt


class Register(Resource):
    def post(self):
        data = request.get_json()
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        dob = data["dob"]
        gender = data["gender"]
        current_time = datetime.now()
        # print("cur time :", current_time)

        if email == '' or password == '':
            abort(400, 'Bad Request')

        # check if user of given email already exists
        CHECK_EMAIL = 'SELECT id FROM users WHERE email= %s'
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            print("cursor object:", cursor, "\n")

            cursor.execute(CHECK_EMAIL, (email,))
            row = cursor.fetchone()
            if row is not None:
                abort(400, 'Bad Request')
        except (Exception, psycopg2.Error) as err:
            print(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()

        # user doesn't exists..now create user with hashed password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        hashed_password = hashed_password.decode('utf-8')

        REGISTER_USER = '''INSERT INTO users(name, email, phone, password, dob, gender, added_at) 
        VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            print("cursor object:", cursor, "\n")

            cursor.execute(REGISTER_USER, (name, email, phone,
                           hashed_password, dob, gender, current_time,))
            user_id = cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as err:
            print(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()

        # todo: generate token pair

        # when authenticated, return a fresh access token and a refresh token
        # print(f_jwt)
        access_token = f_jwt.create_access_token(identity=user_id, fresh=True)
        refresh_token = f_jwt.create_refresh_token(user_id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201
        # return response, 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        if email == '' or password == '':
            abort(400, 'Bad Request')

        # check if user of given email already exists
        GET_USER = 'SELECT id, password FROM users WHERE email= %s'
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            print("cursor object:", cursor, "\n")

            cursor.execute(GET_USER, (email,))
            row = cursor.fetchone()
            if row is None:
                abort(400, 'Bad Request: User not found')
            else:
                user_id = row[0]
                hashed_password = row[1]
        except (Exception, psycopg2.Error) as err:
            print(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()

        # check user's entered password's hash with db's stored hashed password
        if (bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')) == False):
            abort(400, 'Email or password not correct')

        # todo: generate token pair
        access_token = f_jwt.create_access_token(identity=user_id, fresh=True)
        refresh_token = f_jwt.create_refresh_token(user_id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 202
        return {"message": "Status accepted"}, 202


class RefreshToken(Resource):
    @f_jwt.jwt_required(refresh=True)
    def post(self):
        # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
        current_user_id = f_jwt.get_jwt_identity()

        # return a non-fresh token for the user
        new_token = f_jwt.create_access_token(identity=current_user_id, fresh=False)
        return {'access_token': new_token}, 200