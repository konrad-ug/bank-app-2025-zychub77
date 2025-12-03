import pytest
from app.api import *
from src.AccountRegistry import AccountRegistry


@pytest.fixture
def client():
    registry.accounts = []
    return app.test_client()


class TestAccountsAPI:

    def test_create_account(self, client):
        response = client.post(
            "/api/accounts",
            json={"name": "Alice", "last_name": "Smith", "pesel": "12345678901"},
        )

        assert response.status_code == 201
        assert response.get_json() == {"message": "Account created"}

    def test_create_account_pesel_already_in_use(self, client):
        client.post(
            "/api/accounts",
            json={"name": "John", "last_name": "Doe", "pesel": "05280199999"},
        )
        response = client.post(
            "/api/accounts",
            json={"name": "John", "last_name": "Doe", "pesel": "05280199999"},
        )

        assert response.status_code == 409
        assert response.get_json() == {
            "message": "An account with this PESEL already exists"
        }

    def test_get_all_accounts(self, client):
        client.post("/api/accounts", json={"name": "A", "last_name": "B", "pesel": "1"})
        client.post("/api/accounts", json={"name": "C", "last_name": "D", "pesel": "2"})

        response = client.get("/api/accounts")
        data = response.get_json()

        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]["pesel"] == "Invalid"
        assert data[1]["pesel"] == "Invalid"

    def test_get_account_count(self, client):
        client.post("/api/accounts", json={"name": "A", "last_name": "B", "pesel": "1"})
        client.post("/api/accounts", json={"name": "C", "last_name": "D", "pesel": "2"})

        response = client.get("/api/accounts/count")

        assert response.status_code == 200
        assert response.get_json() == {"count": 2}

    def test_get_account_by_pesel(self, client):
        client.post(
            "/api/accounts",
            json={"name": "A", "last_name": "B", "pesel": "05280199999"},
        )

        response = client.get("/api/accounts/05280199999")
        data = response.get_json()

        assert data["pesel"] == "05280199999"
        assert data["first_name"] == "A"
        assert data["last_name"] == "B"

    def test_get_account_by_pesel_not_found(self, client):
        response = client.get("/api/accounts/999")
        data = response.get_json()

        assert data["pesel"] is None

    def test_delete_account(self, client):
        client.post(
            "/api/accounts",
            json={"name": "A", "last_name": "B", "pesel": "05280199999"},
        )

        response = client.delete("/api/accounts/05280199999")
        assert response.status_code == 200

        # Ensure it's gone
        response = client.get("/api/accounts")
        assert response.get_json() == []

    def test_patch_account(self, client):
        client.post(
            "/api/accounts",
            json={"name": "A", "last_name": "B", "pesel": "05280199999"},
        )

        response = client.patch(
            "/api/accounts/05280199999", json={"pesel": "05280299999"}
        )
        assert response.status_code == 200
        assert response.get_json()["message"] == "Account updated"

    def test_patch_account_unknown_pesel(self, client):
        client.post(
            "/api/accounts",
            json={"name": "A", "last_name": "B", "pesel": "123"},
        )

        response = client.patch("/api/accounts/123")
        assert response.status_code == 200
        assert response.get_json()["message"] == "Account updated"
