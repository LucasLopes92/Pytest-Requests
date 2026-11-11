"""Cenários de consulta e criação simulada de produtos."""


def test_list_products_returns_valid_collection(api_client):
    response = api_client.get("/products")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["products"], list)
    assert body["products"]
    assert body["total"] >= len(body["products"])
    assert body["limit"] > 0
    assert body["skip"] == 0


def test_get_product_by_id_returns_expected_product(api_client):
    response = api_client.get("/products/1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert isinstance(body["title"], str) and body["title"]
    assert isinstance(body["price"], (int, float))
    assert body["price"] > 0
    assert body["category"]


def test_product_pagination_respects_limit_and_skip(api_client):
    response = api_client.get("/products", params={"limit": 5, "skip": 10})

    assert response.status_code == 200
    body = response.json()
    assert len(body["products"]) == 5
    assert body["limit"] == 5
    assert body["skip"] == 10


def test_search_products_returns_matching_collection(api_client):
    response = api_client.get("/products/search", params={"q": "phone"})

    assert response.status_code == 200
    body = response.json()
    assert body["products"]
    assert body["total"] >= len(body["products"])
    assert all(isinstance(product["title"], str) for product in body["products"])


def test_add_product_returns_created_product_representation(api_client):
    new_product = {
        "title": "Produto de demonstração QA",
        "price": 19.99,
        "category": "groceries",
    }

    response = api_client.post("/products/add", json=new_product)

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body.get("id"), int)
    assert body["title"] == new_product["title"]
    assert body["price"] == new_product["price"]
