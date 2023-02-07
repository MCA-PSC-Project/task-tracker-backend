from datetime import datetime
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
from flask import current_app as app


class Basket(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
    
        app.logger.debug("user_id= %s", user_id)
        baskets_list = []

        GET_BASKETS = '''SELECT id, product_name, status_type,TO_CHAR(completed_at, 'YYYY-MM-DD'), 
        product_type, repeat FROM baskets WHERE user_id= %s'''
    
        try:

            cursor = main.db_conn.cursor()

            cursor.execute(GET_BASKETS, (user_id,))
            rows = cursor.fetchall()
            if not rows:
                return {}
            for row in rows:
                basket_dict={}
                basket_dict['id'] = row[0]
                basket_dict['product_name'] = row[1]
                basket_dict['status_type'] =row[2]
                basket_dict['completed_at'] =row[3]
                basket_dict['product_type'] =row[4]
                basket_dict['repeat'] =row[5]

                baskets_list.append(basket_dict)
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        app.logger.debug(baskets_list)
        return baskets_list

    @f_jwt.jwt_required()
    def post(self):
        user_id = f_jwt.get_jwt_identity()
        data = request.get_json()
        product_name = data["product_name"]
        status_type = data["status_type"]
        product_type = data["product_type"]
        repeat = data["repeat"]
        current_time = datetime.now()
    
        CREATE_BASKET_RETURN_ID = '''INSERT INTO baskets(user_id, product_name, status_type, added_at, product_type, repeat) 
        VALUES(%s, %s, %s, %s, %s, %s) RETURNING id'''

        try:
    
            cursor = main.db_conn.cursor()

            cursor.execute(CREATE_BASKET_RETURN_ID,
                           (user_id, product_name, status_type, current_time, product_type, repeat,))
            basket_id = cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Basket {product_name} created with id = {basket_id}."}, 201

    @f_jwt.jwt_required()
    def put(self, basket_id):
        data = request.get_json()
        product_name = data["product_name"]
        status_type = data["status_type"]
        completed_at = data["completed_at"]
        product_type = data["product_type"]
        repeat = data["repeat"]
        current_time = datetime.now()
        UPDATE_LIST = '''UPDATE baskets SET product_name= %s, status_type= %s, updated_at= %s, completed_at= %s,
         product_type= %s, repeat=%s WHERE id= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(UPDATE_LIST, (product_name, status_type, current_time, completed_at, product_type, repeat, basket_id,))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Basket {basket_id} modified."}, 200

    @f_jwt.jwt_required()
    def delete(self, basket_id):
        DELETE_BASKET = 'DELETE FROM baskets WHERE id= %s'

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(DELETE_BASKET, (basket_id,))
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return 200
