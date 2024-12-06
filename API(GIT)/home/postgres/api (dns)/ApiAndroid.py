from flask_restful import Resource, reqparse

class User(Resource):
    def get(self, id):
        return {"id": 1, "name": "Дмитрий", "surname": "Азанов"}
        
    def post(self):
        return {"id": 2, "name": "Имя", "surname": "Фамилия"}
