import pytest
from app import app
from database import products_collection


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_test_products():
    products_collection.delete_many({})
    yield
    products_collection.delete_many({})