from flask import Flask
from app.views import supplier, product, order
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/sis_compras'

app.register_blueprint(supplier.bp)
# app.register_blueprint(product.bp)
# app.register_blueprint(order.bp)

mongo = PyMongo(app)
