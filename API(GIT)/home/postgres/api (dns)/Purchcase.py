from flask import Flask, request
from flask_restx import Resource, Api
import datetime
import psycopg2
import psycopg2.extras

app = Flask(__name__)
api = Api(app)

class Purchase(Resource):
    def get(self, id=None):
        groups_list = []
        token = request.args.get('token', default='0')
        customer_id = 0

        # Проверка токена
        try:
            conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(f"SELECT * FROM public.customers WHERE customer_token LIKE '{token}';")

            for row in cursor:
                customer_id = row['customer_id']

            conn.close()

        except Exception as e:
            print(str(e))
            return str(e)
        
        # Если токен корректен
        if customer_id != 0:
            try:
                conn = psycopg2.connect(host='localhost', user='postgres', password='123', dbname='goods2', port='5432')
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                if id is None:
                    # Запрос всех покупок
                    cursor.execute('''
                        SELECT 
                            pu.purchase_id, 
                            pu.purchase_date, 
                            c.customer_id, 
                            c.customer_iname, 
                            c.customer_fname, 
                            c.customer_patr, 
                            c.customer_login, 
                            s.store_id, 
                            s.store_name 
                        FROM 
                            public.purchases AS pu 
                        JOIN 
                            customers AS c ON pu.customer_id = c.customer_id 
                        JOIN 
                            stores AS s ON pu.store_id = s.store_id
                    ''')
                    
                    for row in cursor:
                        purchase_id = row['purchase_id']
                        purchase_date = row['purchase_date']
                        customer = {
                            "customer_id": row['customer_id'],
                            "surname": row['customer_iname'],
                            "name": row['customer_fname'],
                            "patr": row['customer_patr'],
                            "login": row['customer_login']
                        }
                        store = {
                            "store_id": row['store_id'],
                            "store_name": row['store_name']
                        }

                        # Подзапрос для получения товаров
                        cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                        cursor2.execute('''
                            SELECT 
                                pr.product_id, 
                                pr.product_name, 
                                pi.product_price, 
                                pi.product_count, 
                                m.manufacturer_id, 
                                m.manufacturer_name, 
                                c.category_id, 
                                c.category_name 
                            FROM 
                                public.purchase_items AS pi 
                            JOIN 
                                products AS pr ON pr.product_id = pi.product_id 
                            JOIN 
                                manufacturers AS m ON m.manufacturer_id = pr.manufacturer_id 
                            JOIN 
                                categories AS c ON c.category_id = pr.category_id 
                            WHERE 
                                pi.purchase_id = %s
                        ''', (purchase_id,))
                        
                        purchases = []
                        for item in cursor2:
                            purchases.append({
                                "product_id": item['product_id'],
                                "product_name": item['product_name'],
                                "manufacturer_id": item['manufacturer_id'],
                                "manufacturer_name": item['manufacturer_name'],
                                "category_id": item['category_id'],
                                "category_name": item['category_name'],
                                "product_count": item['product_count'],
                                "product_price": float(item['product_price'])
                            })
                        
                        groups_list.append({
                            "purchase_id": purchase_id,
                            "customer": customer,
                            "store": store,
                            "purchase_date": (datetime.datetime.fromtimestamp(purchase_date)).strftime("%Y-%m-%d"),
                            "purchases": purchases
                        })

                else:
                    # Запрос конкретной покупки по ID
                    cursor.execute(f'''
                        SELECT 
                            pu.purchase_id, 
                            pu.purchase_date, 
                            c.customer_id, 
                            c.customer_iname, 
                            c.customer_fname, 
                            c.customer_patr, 
                            c.customer_login, 
                            s.store_id, 
                            s.store_name 
                        FROM 
                            public.purchases AS pu 
                        JOIN 
                            customers AS c ON pu.customer_id = c.customer_id 
                        JOIN 
                            stores AS s ON pu.store_id = s.store_id 
                        WHERE 
                            pu.purchase_id = {id}
                    ''')
                    
                    for row in cursor:
                        purchase_id = row['purchase_id']
                        purchase_date = row['purchase_date']
                        customer = {
                            "customer_id": row['customer_id'],
                            "surname": row['customer_iname'],
                            "name": row['customer_fname'],
                            "patr": row['customer_patr'],
                            "login": row['customer_login']
                        }
                        store = {
                            "store_id": row['store_id'],
                            "store_name": row['store_name']
                        }

                        # Подзапрос для получения товаров
                        cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                        cursor2.execute('''
                            SELECT 
                                pr.product_id, 
                                pr.product_name, 
                                pr.product_price, 
                                pi.product_count, 
                                m.manufacturer_id, 
                                m.manufacturer_name, 
                                c.category_id, 
                                c.category_name 
                            FROM 
                                public.purchase_items AS pi 
                            JOIN 
                                products AS pr ON pr.product_id = pi.product_id 
                            JOIN 
                                manufacturers AS m ON pr.manufacturer_id = m.manufacturer_id 
                            JOIN 
                                categories AS c ON pr.category_id = c.category_id 
                            WHERE 
                                pi.purchase_id = %s
                        ''', (purchase_id,))
                        
                        purchases = []
                        for item in cursor2:
                            purchases.append({
                                "product_id": item['product_id'],
                                "product_name": item['product_name'],
                                "manufacturer_id": item['manufacturer_id'],
                                "manufacturer_name": item['manufacturer_name'],
                                "category_id": item['category_id'],
                                "category_name": item['category_name'],
                                "product_count": item['product_count'],
                                "product_price": float(item['product_price'])
                            })
                        
                        groups_list.append({
                            "purchase_id": purchase_id,
                            "customer": customer,
                            "store": store,
                            "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                            "purchases": purchases
                        })

                conn.close()

            except Exception as e:
                print(str(e))
                return str(e)
        else:
            groups_list.append({"Ошибка": "Не авторизован"})

        return groups_list


api.add_resource(Purchase, '/purchase', '/purchase/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
