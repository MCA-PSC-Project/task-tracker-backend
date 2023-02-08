from datetime import datetime
import json
from flask import request, abort
from flask_restful import Resource
import psycopg2
import app.main as main
import flask_jwt_extended as f_jwt
from flask import current_app as app

# todo:- duration and actual end time


class UserSetting(Resource):
    @f_jwt.jwt_required()
    def get(self):
        user_id = f_jwt.get_jwt_identity()
        # user_id=20
        app.logger.debug("user_id= %s", user_id)

        GET_SETTING = '''SELECT id, user_id, theme_type, theme_color, background_image_id, 
        confirm_deletion, top_task_type, notify, mode 
        FROM users_settings WHERE user_id= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(GET_SETTING, (user_id,))
            row = cursor.fetchone()
            if not row:
                return abort(404, "Not Found")
            setting_dict = {}
            setting_dict['id'] = row[0]
            setting_dict['user_id'] = row[1]
            setting_dict['theme_type'] = row[2]
            setting_dict['theme_color'] = row[3]
            setting_dict['background_image_id'] = row[4]
            setting_dict['confirm_deletion'] = row[5]
            setting_dict['top_task_type'] = row[6]
            setting_dict['notify'] = row[7]
            setting_dict['mode'] = row[8]
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        app.logger.debug(setting_dict)
        return setting_dict

    @f_jwt.jwt_required()
    def put(self, setting_id):
        user_id = f_jwt.get_jwt_identity()
        # user_id=20
        app.logger.debug("user_id= %s", user_id)

        data = request.get_json()
        setting_dict = json.loads(json.dumps(data))
        # current_time = datetime.now()
        # app.logger.debug("cur time : %s", current_time)

        UPDATE_SETTING = '''UPDATE users_settings SET theme_type= %s, theme_color= %s, background_image_id= %s,
        confirm_deletion= %s ,top_task_type= %s ,notify= %s ,mode= %s
        WHERE id= %s AND user_id= %s'''

        # catch exception for invalid SQL statement
        try:
            # declare a cursor object from the connection
            cursor = main.db_conn.cursor()
            # app.logger.debug("cursor object: %s", cursor)

            cursor.execute(UPDATE_SETTING, (setting_dict['theme_type'], setting_dict['theme_color'],
                                            setting_dict['background_image_id'], setting_dict['confirm_deletion'],
                                            setting_dict['top_task_type'], setting_dict['notify'],
                                            setting_dict['mode'], setting_id, user_id,))
            # app.logger.debug("row_counts= %s", cursor.rowcount)
            if cursor.rowcount != 1:
                abort(400, 'Bad Request: update row error')
        except (Exception, psycopg2.Error) as err:
            app.logger.debug(err)
            abort(400, 'Bad Request')
        finally:
            cursor.close()
        return {"message": f"Setting of id= {setting_id} modified."}, 200


class ResetUserSetting(Resource):
    pass
