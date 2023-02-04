from datetime import datetime
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main


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
        hashed_password = main.bcrypt.generate_password_hash(
            password).decode('utf-8')
        print(hashed_password)

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
        return {"message": f"User {name} created with id = {user_id}."}, 201


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

        print(hashed_password)
        print(password)
        # check user's entered password's hash with db's stored hashed password
        result = main.bcrypt.check_password_hash(hashed_password, password)
        print(result)
        if result == False:
            abort(400, 'Email or password not correct')

        # todo: generate token pair
        return {"message": "Status accepted"}, 202


class Refresh(Resource):
    pass
