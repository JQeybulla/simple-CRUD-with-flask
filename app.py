from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)

# init marhsmallow
ma = Marshmallow(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

# Product Schema
class  ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Create a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_product = Product(name, description, price, quantity)
    
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product) 

# list of all products
@app.route("/product", methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Single product
@app.route("/product/<id>", methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# update a product
@app.route('/update/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()

    return product_schema.jsonify(product)

# delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({"msg":"Product Deleted!"})

# runserver
if __name__ == '__main__':
    app.run(debug=True)