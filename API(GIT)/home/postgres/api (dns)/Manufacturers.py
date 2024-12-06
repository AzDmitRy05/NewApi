from flask import Flask, request
from flask_restx import Resource, Api

import psycopg2
import psycopg2.extras

class Manufacturers(Resource):
    def get(self):
        groups_list = []
        token = request.args.get('token', default='0')
        customer_id=0
        try:
                    conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute(f'''SELECT * FROM public.customers WHERE customer_token like '{token}';''')
                    
                    for row in cursor:
                        customer_id = row['customer_id']
                        
                    conn.close()
                  
        except Exception as e:
                    print(str(e))
                    return str(e)
        if(customer_id!=0):
            
            try:
                    conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute('SELECT * FROM public.manufacturers ORDER BY manufacturer_id ASC ')
                    for row in cursor:
                        id = row['manufacturer_id']
                        name = row['manufacturer_name']
                
                        groups_list.append({'id': id, 'name': name})
                    conn.close()
            except Exception as e:
                    print(str(e))
                    return str(e)
        else:
                groups_list.append({"Ошибка":"Не авторизироаван"})
        return groups_list