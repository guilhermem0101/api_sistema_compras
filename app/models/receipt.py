def create_receipt(receipt_data):
    from app import mongo
    return mongo.db.recebimento.insert_one(receipt_data)


def get_receipt(receipt_id):
    from app import mongo
    return mongo.db.recebimento.find_one({'_id': receipt_id})


def get_all_receipts():
    from app import mongo
    return mongo.db.recebimento.find()


def update_receipt(receipt_id, update_data):
    from app import mongo
    return mongo.db.recebimento.update_one({'_id': receipt_id}, {'$set': update_data})


def delete_receipt(receipt_id):
    from app import mongo
    return mongo.db.recebimento.delete_one({'_id': receipt_id})


def get_receipt_counts():
    from app import mongo
    pipeline = [
        {"$unwind": "$recebimentos"},
        {"$unwind": "$recebimentos.fornecedores"},
        {
            "$group": {
                "_id": "$recebimentos.fornecedores.nome",
                "quantidadeEntregas": {"$sum": 1}
            }
        },
        {"$sort": {"quantidadeEntregas": -1}},
        {"$limit": 10}
    ]

    result = mongo.db.recebimento.aggregate(pipeline)

    return list(result)
