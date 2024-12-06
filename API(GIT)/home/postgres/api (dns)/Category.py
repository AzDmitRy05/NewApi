from flask_restx import Resource, reqparse
from flask import Flask, request
import psycopg2
import psycopg2.extras

class Category(Resource):
    def get(self, category_id=None):
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
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='123',
                    dbname='goods2',
                    port='5432'
                )
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                if category_id:
                    cursor.execute('SELECT * FROM categories WHERE category_id = %s', (category_id,))
                else:
                    cursor.execute('SELECT * FROM categories ORDER BY category_name ASC')

                for row in cursor:
                    id = row['category_id']
                    name = row['category_name']
                    logo = row.get('category_logo') 
                    groups_list.append({'id': id, 'name': name, 'logo': logo})

            except Exception as e:
                return {'error': str(e)}, 500
            finally:
                if conn:
                    conn.close()
        else:
            groups_list.append({"Ошибка":"Не авторизироаван"})
        return groups_list
