from flask_restful import Resource


class UserProfile(Resource):
    def get(self):
        return {"user": "prashant"}

    def put(self):
        pass

    def delete(self):
        pass
