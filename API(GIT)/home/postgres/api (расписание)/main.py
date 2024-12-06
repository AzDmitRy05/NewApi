from flask import Flask, request
from flask_restful import Resource, Api
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Response
import hashlib
from datetime import datetime


app = Flask(__name__)
api = Api(app)

# Функция для создания подключения
def get_db_connection():
    global conn
    try:
        # Проверяем активность подключения
        if conn.closed != 0:  # Если соединение закрыто
            conn = psycopg2.connect(
                host="localhost", 
                user="postgres", 
                password="123", 
                dbname="institut", 
                port=5432  
            )
    except Exception as e:
        conn = psycopg2.connect(
            host="localhost", 
            user="postgres", 
            password="123", 
            dbname="institut", 
            port=5432  
        )

# Изначально создаём подключение
conn = psycopg2.connect(
    host="localhost", 
    user="postgres", 
    password="123", 
    dbname="institut", 
    port=5432  
)

class Schedule(Resource):
    def get(self):
        get_db_connection()


        group_name = request.args.get('group')
        teacher = request.args.get('teacher')
        week = request.args.get('week')
        room = request.args.get('room')
        day = request.args.get('day')

        where_clauses = []

        if group_name:
            where_clauses.append(f"g.name = '{group_name}'")
        if teacher:
            where_clauses.append(f"p.teacher_fio = '{teacher}'")
        if week:
            where_clauses.append(f"w.num = {week}")
        if room:
            where_clauses.append(f"r.name = '{room}'")
        if day:
            where_clauses.append(f"d.name = '{day}'")

        where_statement = ""
        if where_clauses:
            where_statement = "WHERE " + " AND ".join(where_clauses)

        query = f"""
        SELECT 
            d.name AS day_name,
            t.tiime AS time,
            sub.num AS subject,
            p.teacher_fio AS teacher,
            STRING_AGG(r.name, ',') AS rooms,
            tp.name AS type,
            g.name AS group_name
        FROM 
            schedule s
            JOIN "GROOUP" g ON s."GROOUP_id" = g.id
            JOIN days d ON s.day_id = d.id
            JOIN tiimes t ON s.time_id = t.id
            JOIN subjects sub ON s.para_id = sub.id
            JOIN prepodi p ON s.prepod_id = p.id
            JOIN schedule_rooms sr ON s.id = sr.id_schedule
            JOIN rooms r ON sr.id_room = r.id
            JOIN types tp ON s.para_type_id = tp.id
            JOIN schedule_week sw ON s.id = sw.id_schedule
            JOIN weeks w ON sw.id_week = w.num
        {where_statement}
        GROUP BY 
            g.name, d.name, d.id, t.tiime, t.id, sub.num, p.teacher_fio, tp.name  -- Добавляем колонки в GROUP BY
        ORDER BY 
            d.id, t.id;

        """

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
            
            sch_list = []

            if results:
                for row in results:
                    group_name = row['group_name']
                    day_name = row['day_name']
                    time = row['time']
                    subject = row['subject']
                    teacher = row['teacher']
                    rooms = row['rooms'].split(',')  # Разделяем кабинеты по запятой
                    type = row['type']

                    sch_list.append({
                        'group_name': group_name,
                        'day_name': day_name,
                        'time': time,
                        'subject': subject,
                        'teacher': teacher,
                        'rooms': rooms,  
                        'type': type
                    })
                return sch_list
            else:
                return {'message': 'No data found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500
        


class Group(Resource):
    def get(self):
        get_db_connection()

        query = 'SELECT * FROM "GROOUP"'
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            sch_list = []

            if results:
                for row in results:
                    sch_list.append({
                        'id': row['id'],  
                        'name': row['name'],
                        'faculty': row['faculty'],
                    })
                return sch_list
            else:
                return {'message': 'No data found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500


class Week(Resource):
    def get(self):
        # Проверяем подключение перед выполнением запроса
        get_db_connection()

        query = "SELECT * FROM weeks"
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            sch_list = []

            if results:
                for row in results:
                    sch_list.append({
                        'num': row['num'],  
                        'date_start': row['date_start'].strftime('%Y-%m-%d'),
                        'date_end': row['date_end'].strftime('%Y-%m-%d'),
                    })
                return sch_list
            else:
                return {'message': 'No data found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500

    
class Prepod(Resource):
    def get(self):
        # Проверяем подключение перед выполнением запроса
        get_db_connection()

        teacher_fio = request.args.get('fio')
        query = f'SELECT * FROM "prepodi" WHERE teacher_fio = %s'
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (teacher_fio,))
                results = cursor.fetchall()

            sch_list = []

            if results:
                for row in results:
                    sch_list.append({
                        'teacher': row['teacher'],  
                        'teacher_fio': row['teacher_fio'],
                        'teacher_link': row['teacher_link'],
                        'teacher_img': row['teacher_img'],
                        'teacher_mail': row['teacher_mail'],
                        'teacher_phone': row['teacher_phone'],
                        'teacher_adress': row['teacher_adress']
                    })
                return sch_list
            else:
                return {'message': 'No data found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500


api.add_resource(Prepod, '/prepod')
api.add_resource(Schedule, '/schedule')
api.add_resource(Group, '/group')
api.add_resource(Week, '/week')

if __name__ == "__main__":
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5000
    )
    
    
    
    
    
#localhost:5000/prepod?fio=Сафаров Рустам Ахтамович
#localhost:5000/schedule?group=ИП-21&week=4
#localhost:5000/group
#localhost:5000/week
