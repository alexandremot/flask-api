
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
                                         basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize database
db = SQLAlchemy(app)

# initialize marshmallow
marshmallow = Marshmallow(app)


# product class/model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


# product schema
class ProductSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


# initialize schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# create a product
@app.route('/product', methods=['POST'])
def add_product():
    # parameters
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    # create a product object
    new_product = Product(name, description, price, quantity)
    # submit to the sql data
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)


# update a product
@app.route('/product/<id>', methods=['PUT'])
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

# get a list containing all products
@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# get single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    just_one_product = Product.query.get(id)
    result = product_schema.jsonify(just_one_product)
    return result

# delete a product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product_to_delete = Product.query.get(id)
    db.session.delete(product_to_delete)
    db.session.commit()
    result = product_schema.jsonify(product_to_delete)
    return result


# run server
if __name__ == '__main__':
    app.run(debug=True)
