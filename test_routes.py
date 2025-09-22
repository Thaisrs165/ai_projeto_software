import pytest
from unittest.mock import patch
from app import app
from datetime import date


@pytest.fixture
def filme():
    app.config["TESTING"] = True
    return app.test_filme() 


@patch("app.criar_objeto_filme")
def test_criar_filme_route(mock_criar, filme):
    mock_criar.return_value = {"id": "123", "titulo": "Jurassic", "descricao": "filme de dinossauro", "duracao": 2, "diretor": "Spilberg", "dataCadastro": date.today()}

    response = filme.post("/filmes", json={"titulo": "Jurassic", "descricao": "filme de dinossauro", "duracao": 2, "diretor": "Spilberg", "dataCadastro": date.today()})
    data = response.get_json()

    assert response.status_code == 201
    assert data["id"] == "123"

def test_criar_filme_route_missing_field(filme):
    response = filme.post("/filmes", json={"titulo": "Jurassic", "descricao": "filme de dinossauro", "duracao": 2, "diretor": "Spilberg", "dataCadastro": date.today()})
    data = response.get_json()
    assert response.status_code == 400
    assert "titulo" in data["erro"]

@patch("app_service.listar_filmes") 
def test_listar_filmes_route(mock_listar, filme):
    mock_listar.return_value = [{"id": "123", "titulo": "Jurassic", "descricao": "filme de dinossauro", "duracao": 2, "diretor": "Spilberg", "dataCadastro": date.today()}]

    response = filme.get("/filmes")
    data = response.get_json()

    assert response.status_code == 200
    assert data[0]["titulo"] == "Jurassic"


@patch("app.deletar_filme") 
def test_deletar_filme_route(mock_deletar, filme):
    mock_deletar.return_value = True

    response = filme.delete("/filmes/123")
    data = response.get_json()

    assert response.status_code == 200
    assert "sucesso" in data["mensagem"]

@patch("app_service.deletar_filme")
def test_deletar_filme_route_not_found(mock_deletar, filme):
    mock_deletar.return_value = False
    response = filme.delete("/filmes/999")
    assert response.status_code == 404