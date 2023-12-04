def create_product(product_data):
    from app import mongo
    return mongo.db.produtos.insert_one(product_data)


def get_product(product_id):
    from app import mongo
    return mongo.db.produtos.find_one({'_id': product_id})


def get_all_products():
    from app import mongo
    return mongo.db.produtos.find()


def get_all_products_name():
    from app import mongo
    return mongo.db.produtos.find({}, {"nome": 1, "fornecedor": 1, "_id": 0})




def update_product(product_id, update_data):
    from app import mongo
    return mongo.db.produtos.update_one({'_id': product_id}, {'$set': update_data})


def delete_product(product_id):
    from app import mongo
    return mongo.db.produtos.delete_one({'_id': product_id})
