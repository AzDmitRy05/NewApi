from flask import Flask
from flask_restx import Api
from Purchcase import Purchase
from autorisation import Autorisation
from Manufacturers import Manufacturers
from Customers import Customers
from Category import Category
from Product import Products
from Login import Login

app = Flask(__name__)
api = Api(app)

api.add_resource(Purchase, '/purchases', "/purchases/<int:id>")
# api.add_resource(Autorisation, '/autorisation')
api.add_resource(Login, '/login')
api.add_resource(Manufacturers, '/manufacturers')
api.add_resource(Customers, '/customers', '/customers/<int:id>')
api.add_resource(Category, '/categories', '/categories/<int:category_id>')
api.add_resource(Products, '/products', '/products/<int:product_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

