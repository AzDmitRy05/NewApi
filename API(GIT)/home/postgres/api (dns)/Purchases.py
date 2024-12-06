from flask_restx import Resource, Namespace
from flask import request
import psycopg2
import psycopg2.extras

ns = Namespace('purchases', description='Оформление заказа')

class Purchase(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {'message': 'Нет данных в запросе'}, 400

        items = data.get('items')
        customer_id = data.get('customer_id')
        store_id = data.get('store_id')
        purchase_date = data.get('purchase_date')

        if not customer_id or not store_id or not purchase_date or not items:
            return {'message': 'Отсутствуют обязательные поля'}, 400

        try:
            conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='123',
                dbname='goods2',
                port='5432'
            )
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                INSERT INTO purchases (customer_id, store_id, purchase_date)
                VALUES (%s, %s, %s)
                RETURNING purchase_id;
            """, (customer_id, store_id, purchase_date))

            purchase_id = cursor.fetchone()['purchase_id']

            for item in items:
                product_id = item.get('product_id')
                product_count = item.get('product_count')
                product_price = item.get('product_price')

                if not product_id or not product_count or not product_price:
                    return {'message': 'Отсутствуют поля товара'}, 400

                cursor.execute("""
                    INSERT INTO purchase_items (purchase_id, product_id, product_count, product_price)
                    VALUES (%s, %s, %s, %s);
                """, (purchase_id, product_id, product_count, product_price))

            conn.commit()
            conn.close()

            response = {
                "customer_id": customer_id,
                "store_id": store_id,
                "purchase_date": purchase_date,
                "items": items
            }

            return response, 201

        except Exception as e:
            print(str(e))
            return {'message': str(e)}, 500

