from flask import Flask, request, jsonify
from app_service import *

app = Flask(__name__)


@app.route("/filmes", methods=["POST"])
def criar_filme():
    data = request.get_json() 

    erro = validar_campos(data)
    if erro:
        return jsonify({"erro": erro}), 400

    filme = criar_objeto_filme(data)
    if not filme:
        return jsonify({"erro": "Filme já cadastrado"}), 400
    return jsonify(filme), 201


@app.route("/filmes", methods=["GET"])
def get_filmes():
    return jsonify(listar_filmes())

@app.route("/filmes/<filme_id>", methods=["DELETE"])
def delete_filme(filme_id):
    ok = deletar_filme(filme_id)
    if not ok:
        return jsonify({"erro": "Filme não encontrado"}), 404
    return jsonify({"mensagem": "Filme deletado com sucesso"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)