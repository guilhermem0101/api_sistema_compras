from bson import ObjectId
from app.models.product import create_product, get_product, get_all_products, update_product, delete_product,  get_all_products_name
from flask import Blueprint, jsonify, request, send_file
import matplotlib.pyplot as plt
import io
import matplotlib
matplotlib.use('Agg')

bp = Blueprint('product', __name__, url_prefix='/api/products')


@bp.route('/', methods=['GET'])
def get_products():
    products_cursor = get_all_products()
    products = [dict(product, _id=str(product['_id']))
              for product in products_cursor]
    return jsonify(products)


@bp.route('/nomes', methods=['GET'])
def get_products():
    products_cursor = get_all_products_name()
    products = [dict(product, _id=str(product['_id']))
                for product in products_cursor]
    return jsonify(products)


@bp.route('/', methods=['POST'])
def create_new_product():
    product_data = request.get_json()
    product_id = create_product(product_data)
    return jsonify({'product_id': str(product_id.inserted_id)})


@bp.route('/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = get_product(product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'message': 'product not found'}), 404


@bp.route('/<product_id>', methods=['PUT'])
def update_product_by_id(product_id):
    update_data = request.get_json()
    result = update_product(product_id, update_data)
    if result.modified_count > 0:
        return jsonify({'message': 'product updated successfully'})
    else:
        return jsonify({'message': 'product not found'}), 404


@bp.route('/<product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    result = delete_product(product_id)
    if result.deleted_count > 0:
        return jsonify({'message': 'product deleted successfully'})
    else:
        return jsonify({'message': 'product not found'}), 404
