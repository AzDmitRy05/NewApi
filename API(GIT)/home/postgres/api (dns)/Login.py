from flask_restful import Resource, reqparse
import psycopg2
import psycopg2.extras
import hashlib
import uuid

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("login", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()

        login = args["login"]
        password = hashlib.md5((args["password"]).encode()).hexdigest()

        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='123',
                dbname='goods2',
                port='5432'
            )
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cursor.execute("SELECT * FROM customers WHERE login = %s AND password = %s;", (login, password))
            user = cursor.fetchone()

            if user:
                random_string = str(uuid.uuid4())
                token = hashlib.md5((login + random_string).encode()).hexdigest()

                cursor.execute("UPDATE customers SET token = %s WHERE customer_id = %s;", (token, user['customer_id']))
                conn.commit()

                user['token'] = token

                return {
                    "status": "Успех",
                    "data": {
                        "customer_id": user["customer_id"],
                        "customer_name": user["customer_name"],
                        "customer_surname": user["customer_surname"],
                        "customer_patronymic": user["customer_patronymic"],
                        "login": user["login"],
                        "token": user["token"]
                    }
                }, 200
            else:
                return {"status": "Ошибка", "message": "Неверный логин или пароль"}, 401

        except Exception as e:
            return {"status": "Ошибка", "message": "Произошла ошибка", "error": str(e)}, 500
        finally:
            conn.close()