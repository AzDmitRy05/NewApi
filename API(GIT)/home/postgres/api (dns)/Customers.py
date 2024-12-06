from flask_restx import Resource, reqparse
import bcrypt
from flask import Flask, request
import psycopg2
import psycopg2.extras
class Customers(Resource):
    def post(self):
        groups_list = []
        
        customer_lname = request.args.get('customer_lname', default='0')
        customer_fname = request.args.get('customer_fname', default='0')
        customer_patr = request.args.get('customer_patr', default='0')
        customer_login = request.args.get('customer_login', default='0')
        customer_pass = request.args.get('customer_pass', default='0').encode("utf-8")
        salt = bcrypt.gensalt()
        customer_pass = bcrypt.hashpw(customer_pass, salt)
        
        if(customer_lname!="0" and customer_fname!="0" and customer_patr!="0" and customer_login!="0" and customer_pass!="0"):
            try:
                    conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
                    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cursor.execute(f'''INSERT INTO public.customers ("customer_iname","customer_fname","customer_patr","customer_login","customer_pass") VALUES('{customer_lname}','{customer_fname}','{customer_patr}','{customer_login}','{customer_pass.decode()}') ''')
                    
                    conn.commit() 
                    conn.close()
                    return {"message": "добавлено"}
            except Exception as e:
                    print(str(e))
                    return str(e)

        return {"message": "ошибка: не указаны параметры"}
        




    def put(self, id):
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
                customer_lname = request.args.get('customer_lname', default='0')
                customer_fname = request.args.get('customer_fname', default='0')
                customer_patr = request.args.get('customer_patr', default='0')
                try:
                        conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
                        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                        if(customer_lname!="0"):
                                cursor.execute(f'''UPDATE public.customers SET customer_iname={customer_lname} WHERE customer_id ={id} ''')
                        if(customer_fname!="0"):
                                cursor.execute(f'''UPDATE public.customers SET customer_fname={customer_fname} WHERE customer_id ={id} ''')
                        if(customer_patr!="0"):
                                cursor.execute(f'''UPDATE public.customers SET customer_patr={customer_patr} WHERE customer_id ={id} ''')
                        print (data)
                        conn.commit() 
                        conn.close()
                except Exception as e:
                        print(str(e))
                        return str(e)
        else:
                groups_list.append({"Ошибка":"Не авторизироаван"})

        return groups_list
            











    def delete(self, id):
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
                        cursor.execute(f'''DELETE FROM public.customers  WHERE customer_id={id}''')
                        print ("deleted")
                        conn.commit() 
                        conn.close()
                except Exception as e:
                        print(str(e))
                        return str(e)
        else:
                groups_list.append({"Ошибка":"Не авторизироаван"})
        return groups_list
        





    def get(self,id=None):
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
                        if id is None:
                                cursor.execute(f'SELECT * FROM public.customers')
                                for row in cursor:
                                        customer_id = row['customer_id']
                                        customer_lname = row['customer_iname']
                                        customer_fname = row['customer_fname']
                                        customer_patr = row['customer_patr']
                                        customer_login = row['customer_login']
                                        groups_list.append({'customer_id': customer_id, 'customer_lname': customer_lname, 'customer_fname': customer_fname, 'customer_patr': customer_patr, 'customer_login': customer_login})

                        else:
                                cursor.execute(f'SELECT * FROM public.customers WHERE customer_id ={str(id)}')
                                for row in cursor:
                                        customer_id = row['customer_id']
                                        customer_lname = row['customer_iname']
                                        customer_fname = row['customer_fname']
                                        customer_patr = row['customer_patr']
                                        customer_login = row['customer_login']
                                        groups_list.append({'customer_id': customer_id, 'customer_lname': customer_lname, 'customer_fname': customer_fname, 'customer_patr': customer_patr, 'customer_login': customer_login})
                        conn.close()
                except Exception as e:
                        print(str(e))
                        return str(e)
        
        else:
                groups_list.append({"Ошибка":"Не авторизироаван"})
        return groups_list
