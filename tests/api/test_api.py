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

    @pytest.mark.parametrize(
        "pesel, outgoing_pesel, amount, type, expected_code, expected_message",
        [
            ("123", None, None, None, 404, "No account found"),
            ("04280199999", None, 500, "incoming", 200, "Transfer received"),
            ("04280199999", None, 500, "outgoing", 404, "No account found"),
            ("04280199999", "02280199999", 500, "outgoing", 200, "Transfer failed"),
            (
                "04280199999",
                "02280199999",
                50,
                "outgoing",
                200,
                "Transfer completed successfully",
            ),
        ],
        ids=[
            "invalid_target_account_transfer",
            "valid_incoming_transfer",
            "invalid_outgoing_account_outgoing_transfer",
            "valid_outgoing_transfer_insufficient_funds",
            "valid_outgoing_transfer_sufficient_funds",
        ],
    )
    def test_transfer(
        self,
        pesel,
        outgoing_pesel,
        amount,
        type,
        expected_code,
        expected_message,
        client,
    ):
        registry.addAccount(PersonalAccount("John", "Doe", "04280199999", "PROM_123"))
        registry.addAccount(PersonalAccount("John", "Doe", "02280199999", "PROM_123"))
        registry.getAccountByPESEL("04280199999").balance = 50
        response = client.post(
            f"api/accounts/{pesel}/transfer",
            json={"type": type, "outgoing_pesel": outgoing_pesel, "amount": amount},
        )

        assert response.status_code == expected_code
        assert response.get_json()["message"] == expected_message


class TestAccountsAPIMocked:

    def test_create_account_uses_registry_add(self, mocker, client):
        mocker.patch("app.api.registry.getAllAccounts", return_value=[])
        add_account = mocker.patch("app.api.registry.addAccount")

        response = client.post(
            "/api/accounts",
            json={"name": "Alice", "last_name": "Smith", "pesel": "12345678901"},
        )

        assert response.status_code == 201
        add_account.assert_called_once()
        created_account = add_account.call_args.args[0]
        assert created_account.first_name == "Alice"
        assert created_account.last_name == "Smith"
        assert created_account.pesel == "12345678901"

    def test_create_account_duplicate_pesel_skips_add(self, mocker, client):
        existing = mocker.Mock()
        existing.pesel = "12345678901"
        mocker.patch("app.api.registry.getAllAccounts", return_value=[existing])
        add_account = mocker.patch("app.api.registry.addAccount")

        response = client.post(
            "/api/accounts",
            json={"name": "Alice", "last_name": "Smith", "pesel": "12345678901"},
        )

        assert response.status_code == 409
        add_account.assert_not_called()

    def test_get_account_count_uses_registry(self, mocker, client):
        mocker.patch("app.api.registry.getNumberOfAccounts", return_value=7)

        response = client.get("/api/accounts/count")

        assert response.status_code == 200
        assert response.get_json() == {"count": 7}

    def test_get_account_by_pesel_not_found(self, mocker, client):
        mocker.patch("app.api.registry.getAccountByPESEL", return_value=None)

        response = client.get("/api/accounts/999")

        assert response.status_code == 200
        assert response.get_json()["pesel"] is None

    def test_transfer_incoming_calls_receive_transfer(self, mocker, client):
        account = mocker.Mock()
        mocker.patch("app.api.registry.getAccountByPESEL", return_value=account)

        response = client.post(
            "/api/accounts/123/transfer",
            json={"type": "incoming", "outgoing_pesel": None, "amount": 50},
        )

        assert response.status_code == 200
        assert response.get_json()["message"] == "Transfer received"
        account.receive_transfer.assert_called_once_with(50)

    def test_transfer_outgoing_calls_make_transfer(self, mocker, client):
        incoming_account = mocker.Mock()
        outgoing_account = mocker.Mock()
        incoming_account.make_transfer.return_value = True
        mocker.patch(
            "app.api.registry.getAccountByPESEL",
            side_effect=[incoming_account, outgoing_account],
        )

        response = client.post(
            "/api/accounts/123/transfer",
            json={"type": "outgoing", "outgoing_pesel": "456", "amount": 50},
        )

        assert response.status_code == 200
        assert response.get_json()["message"] == "Transfer completed successfully"
        incoming_account.make_transfer.assert_called_once_with(50, outgoing_account)
