from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_read_root():
    res = client.get("/")
    assert res.status_code == 200


def post_and_assert(route, a, b, expected):
    res = client.post(route, json={"a": a, "b": b})
    assert res.status_code == 200
    assert res.json()["result"] == expected


def test_add_endpoint():
    post_and_assert("/add", 1, 2, 3)


def test_subtract_endpoint():
    post_and_assert("/subtract", 5, 3, 2)


def test_multiply_endpoint():
    post_and_assert("/multiply", 2, 3, 6)


def test_divide_endpoint():
    post_and_assert("/divide", 8, 2, 4.0)


def test_divide_by_zero_endpoint():
    res = client.post("/divide", json={"a": 1, "b": 0})
    assert res.status_code == 400
    assert "Cannot divide by zero" in res.json()["error"]
