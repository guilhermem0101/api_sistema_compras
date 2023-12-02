from flask import Flask
from app.views import supplier, product, order, receipt
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/sis_compras'

app.register_blueprint(supplier.bp)
app.register_blueprint(receipt.bp)
# app.register_blueprint(product.bp)
app.register_blueprint(order.bp)

mongo = PyMongo(app)
