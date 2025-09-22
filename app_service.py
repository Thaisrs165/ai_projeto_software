from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from bson.errors import InvalidId

MONGO_URI = "mongodb+srv://admin:5gdstXZdV8boRX8Y@progeficaz.bjvjo.mongodb.net/" 
filme = MongoClient(MONGO_URI)
db = filme["filme_db"]  
filmes_collection = db["filmes"] 

filmes_collection.create_index("titulo", unique=True)

def validar_campos(data):
    campos_obrigatorios = ["titulo", "descricao", "duracao", "diretor", "dataCadastro"]
    for campo in campos_obrigatorios:
        if campo not in data:
            return f"Campo obrigatório '{campo}' não informado"
    return None

def criar_objeto_filme(data):
    try:
        result = filmes_collection.insert_one({
            "titulo": data["titulo"],
            "descricao": data["descricao"],
            "duracao": data["duracao"],
            "diretor": data["diretor"],
            "dataCadastro": data["dataCadastro"],
        })
        return {"id": str(result.inserted_id), "titulo": data["titulo"], "descricao": data["descricao"], "duracao": data["duracao"], "diretor": data["diretor"],"dataCadastro": data["dataCadastro"]}
    except DuplicateKeyError: 
        return None

def listar_filmes():
    filmes = filmes_collection.find()
    return [{"id": str(c["_id"]), "titulo": f["titulo"], "descricao": f["descricao"], "duracao": f["duracao"], "diretor": f["diretor"], "dataCadastro": f["dataCadastro"]} for f in filmes]


def deletar_filme(filme_id):
    try:
        obj_id = ObjectId(filme_id)  
    except InvalidId:
        return False 

    result = filmes_collection.delete_one({"_id": obj_id})
    return result.deleted_count > 0 