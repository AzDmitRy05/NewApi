import ast
import datetime
import random
import re
import smtplib
import bcrypt
from flask import request
from flask_restx import Resource
import psycopg2
from psycopg2 import extras
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def apikeygen():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = random.randint(15, 35)
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

class Autorisation(Resource):
    def post(self):
        password = request.args.get('password', default='0').encode('utf-8')
        login = request.args.get('login', default='0')
        answ = []

        APIKEY = 0
        try:
            # Подключение к базе данных
            conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
            cursor = conn.cursor(cursor_factory=extras.DictCursor)

            # Выполнение запроса для получения данных пользователя
            cursor.execute("""SELECT * FROM public.customers WHERE customer_login = %s""",(login,))
            row = cursor.fetchone()
            print("резулт "+str(row))
            if row is not None:
                customer_name = row['customer_iname']
                customer_fname = row['customer_fname']
                customer_patr = row['customer_patr']
                
                # Получаем хэш пароля из базы данных
                bytes_user_input = row['customer_pass']
                bytes_user_input = bytes(bytes_user_input)

                # Проверка пароля с помощью bcrypt
                if bcrypt.checkpw(password, bytes_user_input):
                    APIKEY = apikeygen()
                    # Обновление токена для пользователя
                    cursor.execute("""UPDATE public.customers SET customer_token = %s WHERE customer_login = %s""",(login,))
                    conn.commit()
                    answ= ({"apikey": APIKEY})
                else:
                    answ=({'error': "Неверный пароль"})
            else:
                answ=({'error': "Пользователь не найден"})

            conn.close()
            return answ

        except Exception as e:
            print(str(e))
            return {'error': str(e)}
