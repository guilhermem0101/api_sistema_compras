from flask import Blueprint, jsonify, request
from app.models.supplier import create_supplier, get_supplier, get_all_suppliers, update_supplier, delete_supplier
from bson import ObjectId
bp = Blueprint('supplier', __name__, url_prefix='/api/suppliers')


@bp.route('/', methods=['GET'])
def get_suppliers():
    suppliers_cursor = get_all_suppliers()
    suppliers = [dict(supplier, _id=str(supplier['_id']))
                 for supplier in suppliers_cursor]
    return jsonify( suppliers)

@bp.route('/', methods=['POST'])
def create_new_supplier():
    supplier_data = request.get_json()
    supplier_id = create_supplier(supplier_data)
    return jsonify({'supplier_id': str(supplier_id.inserted_id)})


@bp.route('/<supplier_id>', methods=['GET'])
def get_supplier_by_id(supplier_id):
    supplier = get_supplier(supplier_id)
    if supplier:
        return jsonify(supplier)
    else:
        return jsonify({'message': 'Supplier not found'}), 404


@bp.route('/<supplier_id>', methods=['PUT'])
def update_supplier_by_id(supplier_id):
    update_data = request.get_json()
    result = update_supplier(supplier_id, update_data)
    if result.modified_count > 0:
        return jsonify({'message': 'Supplier updated successfully'})
    else:
        return jsonify({'message': 'Supplier not found'}), 404


@bp.route('/<supplier_id>', methods=['DELETE'])
def delete_supplier_by_id(supplier_id):
    result = delete_supplier(supplier_id)
    if result.deleted_count > 0:
        return jsonify({'message': 'Supplier deleted successfully'})
    else:
        return jsonify({'message': 'Supplier not found'}), 404
