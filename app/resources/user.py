from flask_restful import Resource


class User(Resource):
    # def get(self):
    #     return {"user": "prashant"}

    def get(self):
        return {"user": "prashant"}

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
