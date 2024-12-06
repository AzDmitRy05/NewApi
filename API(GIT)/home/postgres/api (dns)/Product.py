from flask_restx import Resource, reqparse
from flask import Flask, request
import psycopg2
import psycopg2.extras

class Products(Resource):  
    def post(self):
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
            groups_list = []
            prodname = request.args.get('product_name', default='0')
            manufacturer_id = request.args.get('manufacturer_id', default='0')
            category_id = request.args.get('category_id', default='0')
            if (prodname!=0 and manufacturer_id!=0 and category_id!=0 and isinstance(int(manufacturer_id),int) and isinstance(int(category_id),int)):
                
                try:
                    conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute(f'''INSERT INTO public.products ("product_name","manufacturer_id","category_id") VALUES('{prodname}',{manufacturer_id},{category_id}) ''')
                    conn.commit() 
                    conn.close()
                    groups_list.append({'msg': "Успешно добавлено"}) 
                except Exception as e:
                    print(str(e))
                    return str(e)
            else:
                groups_list.append({'error': "Один из параметров get запроса указан неверно или не указан"}) 
            return groups_list
        else:
            groups_list.append({"Ошибка":"Не авторизироаван"})
    

    def get(self):
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
            groups_list = []
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='123',
                    dbname='goods2',
                    port='5432'
                )
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute('''SELECT * FROM public.products as p 
                                JOIN categories as c ON p.category_id = c.category_id
                                JOIN manufacturers as m ON p.manufacturer_id = m.manufacturer_id;''')
                for row in cursor:
                    id = row['product_id']
                    name = row['product_name']
                    mid = row['manufacturer_id']
                    cid = row['category_id']
                    cname = row['category_name']
                    mname = row['manufacturer_name']
                    groups_list.append({
                        'id': id,
                        'name': name,
                        'manufacturer_id': mid,
                        "manufacturer_name": mname,
                        "category_id": cid,
                        "category_name": cname
                    })
            except Exception as e:
                print(str(e))
                return {'error': str(e)}, 500
            finally:
                if conn:
                    conn.close()

            return groups_list
        else:
            groups_list.append({"Ошибка":"Не авторизироаван"})

    def delete(self, product_id):
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
                cursor = conn.cursor()
                cursor.execute('DELETE FROM products WHERE product_id = %s RETURNING *', (product_id,))
                deleted_row = cursor.fetchone()
                conn.commit()

                if deleted_row:
                    return {'message': f'Product with ID {product_id} deleted successfully.'}, 200
                else:
                    return {'message': f'Product with ID {product_id} not found.'}, 404

            except Exception as e:
                return {'error': str(e)}, 500
            finally:
                if conn:
                    conn.close()
        else:
            groups_list.append({"Ошибка":"Не авторизироаван"})

    def put(self, product_id):
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
            groups_list = []
            prodname = request.args.get('product_name', default='0')
            manufacturer_id = request.args.get('manufacturer_id', default='0')
            category_id = request.args.get('category_id', default='0')
            try:
                    conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    if(prodname!=0):
                        cursor.execute(f'''UPDATE public.products SET product_name='{prodname}' WHERE product_id ={product_id} ''')
                    if(prodname!=0):
                        cursor.execute(f'''UPDATE public.products SET manufacturer_id={manufacturer_id} WHERE product_id ={product_id} ''')
                    if(prodname!=0):
                        cursor.execute(f'''UPDATE public.products SET category_id={category_id} WHERE product_id ={product_id} ''')
                    else:
                        return {'message': f'Не указаны обновления.'}, 200
                    conn.commit() 
                    conn.close()
            except Exception as e:
                    print(str(e))
                    return str(e)

            return groups_list
        else:
            groups_list.append({"Ошибка":"Не авторизироаван"})
