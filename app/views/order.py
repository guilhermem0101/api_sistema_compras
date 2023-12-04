from app.models.order import create_order, get_order, get_all_orders, update_order, delete_order, get_order_avg_days, purchase_history
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Blueprint, jsonify, request, send_file
from bson import ObjectId

bp = Blueprint('order', __name__, url_prefix='/api/orders')


@bp.route('/', methods=['GET'])
def get_orders():
    orders_cursor = get_all_orders()
    orders = [dict(order, _id=str(order['_id']))
                for order in orders_cursor]
    return jsonify(orders)


@bp.route('/', methods=['POST'])
def create_new_order():
    order_data = request.get_json()
    order_id = create_order(order_data)
    return jsonify({'order_id': str(order_id.inserted_id)})


@bp.route('/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order = get_order(order_id)
    if order:
        return jsonify(order)
    else:
        return jsonify({'message': 'order not found'}), 404


@bp.route('/<order_id>', methods=['PUT'])
def update_order_by_id(order_id):
    update_data = request.get_json()
    result = update_order(order_id, update_data)
    if result.modified_count > 0:
        return jsonify({'message': 'order updated successfully'})
    else:
        return jsonify({'message': 'order not found'}), 404


@bp.route('/<order_id>', methods=['DELETE'])
def delete_order_by_id(order_id):
    result = delete_order(order_id)
    if result.deleted_count > 0:
        return jsonify({'message': 'order deleted successfully'})
    else:
        return jsonify({'message': 'order not found'}), 404


@bp.route('/avg_by_supplier', methods=['GET'])
def get_order_avg_supplier():
    orders_cursor = get_order_avg_days()
    suppliers = [order['_id'] for order in orders_cursor]
    agv_days = [order['mediaDias']
                       for order in orders_cursor]

    plt.bar(suppliers, agv_days)
    plt.xlabel('Fornecedor')
    plt.ylabel('média de dias')
    plt.title('Prazo Médio de Entrega')
    plt.xticks(rotation=45)
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.clf()
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')
