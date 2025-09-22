import pytest
from unittest.mock import MagicMock, patch
from app_service import *
from datetime import date

def test_validar_campos_ok():
    data = {"titulo": "Jurassic", "descricao": "filme de dinossauro", "duracao": 2, "diretor": "Spilberg", "dataCadastro": date.today()}
    assert validar_campos(data) is None

def test_validar_campos_faltando():
    data = {"titulo": "Jurassic", "duracao": 2, "diretor": "Spilberg", "dataCadastro": date.today()}
    erro = validar_campos(data)
    assert "descricao" in erro

@patch("app_service.filmes_collection") 
def test_criar_objeto_filme(mock_collection):
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "123"
    mock_collection.insert_one.return_value = mock_insert_result

    result = criar_objeto_filme({"titulo": "Jurassic", "descricao": "filme de dinossauro", "duracao": 2, "diretor": "Spilberg", "dataCadastro": date.today()})

    assert result["id"] == "123"
    assert result["titulo"] == "Jurassic"
    mock_collection.insert_one.assert_called_once()

@patch("app_service.filmes_collection")
def test_listar_filmes(mock_collection):
    mock_collection.find.return_value = [
        {"_id": "123", "titulo": "Jurassic", "descricao": "filme de dinossauro", "duracao": 2, "diretor": "Spilberg", "dataCadastro": date.today()}
    ]

    result = listar_filmes()
    assert len(result) == 1
    assert result[0]["titulo"] == "Jurassic"

@patch("app_service.ObjectId") 
@patch("app_service.filmes_collection")
def test_deletar_filme(mock_collection, mock_objectid):
    mock_objectid.return_value = "fake_id"

    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    mock_collection.delete_one.return_value = mock_delete_result

    ok = deletar_filme("123")

    assert ok is True