from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_post_valid_reservation_when_database_is_empty():
    params = {
        "at": "2024-07-13T14:35:00.123Z",
        "email": "kazuki@example.com",
        "name": "Kazuki Yoshida",
        "quantity": 4,
    }
