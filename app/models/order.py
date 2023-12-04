

def create_order(order_data):
    from app import mongo
    return mongo.db.itens_pedidos.insert_one(order_data)


def get_order(order_id):
    from app import mongo
    return mongo.db.itens_pedidos.find_one({'_id': order_id})


def get_all_orders():
    from app import mongo
    return mongo.db.itens_pedidos.find()


def update_order(order_id, update_data):
    from app import mongo
    return mongo.db.itens_pedidos.update_one({'_id': order_id}, {'$set': update_data})


def delete_order(order_id):
    from app import mongo
    return mongo.db.itens_pedidos.delete_one({'_id': order_id})


def get_order_avg_days():
   from app import mongo
   pipeline = [
       {
           "$lookup": {
               "from": "recebimento",
               "localField": "pedido",
               "foreignField": "recebimentos.id_pedido",
               "as": "dados_entrega"
           }
       },
       {"$unwind": "$dados_entrega"},
       {"$unwind": "$dados_entrega.recebimentos"},
       {"$unwind": "$dados_entrega.recebimentos.fornecedores"},
       {
           "$project": {
               "subtotal": 1,
               "data": 1,
               "fornecedor": "$dados_entrega.recebimentos.fornecedores.nome",
               "entrega": "$dados_entrega.dataentrega",
               "dias": {
                   "$divide": [
                       {
                          "$subtract": ["$dados_entrega.dataentrega", "$data"]
                       },
                       1000 * 60 * 60 * 24
                   ]
               }
           }
       },
       {
           "$group": {
               "_id": "$fornecedor",
               "avgDias": {"$avg": "$dias"}
           }
       },
       {
           "$project": {
               "_id": 1,
               "mediaDias": {"$toInt": "$avgDias"}
           }
       },
       {"$sort": {"mediaDias": 1}},
       {"$limit": 10}
   ]
   result = mongo.db.itens_pedidos.aggregate(pipeline)
   return list(result)


def purchase_history():
   from app import mongo
   return mongo.db.itens_pedidos.find({}, {'subtotal': 1, 'data': 1, '_id': 0}).sort('data', 1)
