

def create_supplier(supplier_data):
    from app import mongo
    return mongo.db.fornecedores.insert_one(supplier_data)


def get_supplier(supplier_id):
    from app import mongo
    return mongo.db.fornecedores.find_one({'_id': supplier_id})


def get_all_suppliers():
    from app import mongo
    return mongo.db.fornecedores.find()


def get_supplier_byName(receipt_name):
    from app import mongo
    return mongo.db.fornecedores.find({'Nome': {'$regex': receipt_name, '$options': 'i'}})

def update_supplier(supplier_id, update_data):
    from app import mongo
    return mongo.db.suppliers.update_one({'_id': supplier_id}, {'$set': update_data})


def delete_supplier(supplier_id):
    from app import mongo
    return mongo.db.suppliers.delete_one({'_id': supplier_id})
