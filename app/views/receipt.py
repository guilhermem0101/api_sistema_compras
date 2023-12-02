from flask import Blueprint, jsonify, request, send_file
from app.models.receipt import create_receipt, get_receipt, get_all_receipts, update_receipt, delete_receipt, get_receipt_counts
from bson import ObjectId
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
bp = Blueprint('receipt', __name__, url_prefix='/api/receipts')


@bp.route('/', methods=['GET'])
def get_receipts():
    receipts_cursor = get_all_receipts()
    receipts = [dict(receipt, _id=str(receipt['_id']))
                 for receipt in receipts_cursor]
    return jsonify(receipts)


@bp.route('/', methods=['POST'])
def create_new_receipt():
    receipt_data = request.get_json()
    receipt_id = create_receipt(receipt_data)
    return jsonify({'receipt_id': str(receipt_id.inserted_id)})


@bp.route('/<receipt_id>', methods=['GET'])
def get_receipt_by_id(receipt_id):
    receipt = get_receipt(receipt_id)
    if receipt:
        return jsonify(receipt)
    else:
        return jsonify({'message': 'receipt not found'}), 404



@bp.route('/<receipt_id>', methods=['PUT'])
def update_receipt_by_id(receipt_id):
    update_data = request.get_json()
    result = update_receipt(receipt_id, update_data)
    if result.modified_count > 0:
        return jsonify({'message': 'receipt updated successfully'})
    else:
        return jsonify({'message': 'receipt not found'}), 404


@bp.route('/<receipt_id>', methods=['DELETE'])
def delete_receipt_by_id(receipt_id):
    result = delete_receipt(receipt_id)
    if result.deleted_count > 0:
        return jsonify({'message': 'receipt deleted successfully'})
    else:
        return jsonify({'message': 'receipt not found'}), 404


@bp.route('/counts_by_supplier', methods=['GET'])
def counts_by_supplier_counts():
    receipts_cursor = get_receipt_counts()
    suppliers = [receipt['_id'] for receipt in receipts_cursor]
    delivery_counts = [receipt['quantidadeEntregas']
                       for receipt in receipts_cursor]

    plt.bar(suppliers, delivery_counts)
    plt.xlabel('Fornecedor')
    plt.ylabel('Número de Entregas')
    plt.title('Número de Entregas por Fornecedor')
    plt.xticks(rotation=45)
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
  
  # Codifica o buffer da imagem em base64
    return send_file(img_buffer, mimetype='image/png')

