
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import psycopg2


# inicializa app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/hotel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# inicializa database
db = SQLAlchemy(app)
# inicializa marshmallow
marshmallow = Marshmallow(app)


# class/model pedido
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa = db.Column(db.Integer)
    pedido = db.Column(db.String)
    quantidade = db.Column(db.Integer)
    atendente = db.Column(db.String(100))

    def __init__(self, mesa, pedido, quantidade, atendente):
        self.mesa = mesa
        self.pedido = pedido
        self.quantidade = quantidade
        self.atendente = atendente


# schema pedido
class PedidoSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'mesa', 'pedido', 'quantidade', 'atendente')


# inicializa schema pedido
pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)

# gera/inclui um pedido
@app.route('/create_pedido', methods=['POST'])
def create_pedido():
    mesa = request.json['mesa']
    pedido = request.json['pedido']
    quantidade = request.json['quantidade']
    atendente = request.json['atendente']

    novo_pedido = Pedido(mesa, pedido, quantidade, atendente)
    db.session.add(novo_pedido)
    db.session.commit()
    return pedido_schema.jsonify(novo_pedido)


# atualiza/corrige pedido
@app.route('/update_pedido/<id>', methods=['PUT'])
def update_pedido(id):
    pedido = Pedido.query.get(id)

    mesa_atualizada = request.json['mesa']
    pedido_atualizado = request.json['pedido']
    quantidade_atualizada = request.json['quantidade']
    atendente_atualizado = request.json['atendente']

    pedido.mesa = mesa_atualizada
    pedido.pedido = pedido_atualizado
    pedido.quantidade = quantidade_atualizada
    pedido.atendente = atendente_atualizado

    db.session.commit()
    return pedido_schema.jsonify(pedido)

# obtém a relação de todos os pedidos
@app.route('/get_pedidos', methods=['GET'])
def get_pedidos():
    relacao_de_pedidos = Pedido.query.all()
    resultado = pedidos_schema.dump(relacao_de_pedidos)
    return jsonify(resultado)

# obtém os dados de um pedido específico
@app.route('/get_pedido/<id>', methods=['GET'])
def get_pedido(id):
    dados_do_pedido = Pedido.query.get(id)
    resultado = pedido_schema.jsonify(dados_do_pedido)
    return resultado

# deleta um pedido
@app.route('/delete_pedido/<id>', methods=['DELETE'])
def delete_pedido(id):
    pedido_a_deletar = Pedido.query.get(id)
    db.session.delete(pedido_a_deletar)
    db.session.commit()
    resultado = pedido_schema.jsonify(pedido_a_deletar)
    return resultado


# inicializa app
if __name__ == '__main__':
    app.run(debug=True)
