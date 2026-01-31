from src.CompanyAccount import CompanyAccount
import pytest
import os


class TestCompanyAccount:
    @pytest.fixture
    def active_nip_response(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        return mock_resp

    @pytest.fixture
    def unregistered_nip_response(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.json.return_value = {"result": {"subject": None}}
        return mock_resp

    @pytest.fixture
    def account(self, mocker, active_nip_response):
        mocker.patch("src.CompanyAccount.requests.get", return_value=active_nip_response)
        account = CompanyAccount("żabka", "8461627563")
        return account

    @pytest.fixture
    def account2(self, mocker, active_nip_response):
        mocker.patch("src.CompanyAccount.requests.get", return_value=active_nip_response)
        account2 = CompanyAccount("biedronka", "8461627563")
        return account2

    def test_account_creation(self, account):
        assert account.company_name == "żabka"
        assert account.NIP == "8461627563"

    def test_account_NIP_validation(self):
        account3 = CompanyAccount("lidl", "123")
        assert account3.NIP == "Invalid"

    def test_account_NIP_unregistered(self, mocker, unregistered_nip_response):
        mocker.patch.dict(
            os.environ, {"BANK_APP_MF_URL": "https://example.test/api/search/nip/"}
        )
        mocker.patch(
            "src.CompanyAccount.requests.get", return_value=unregistered_nip_response
        )
        try:
            account = CompanyAccount("żabka", "1111111111")
        except ValueError as error:
            assert str(error) == "Company not registered!!"

    def test_account_NIP_inactive(self, mocker, unregistered_nip_response):
        mocker.patch.dict(
            os.environ, {"BANK_APP_MF_URL": "https://example.test/api/search/nip/"}
        )
        mocker.patch(
            "src.CompanyAccount.requests.get", return_value=unregistered_nip_response
        )
        try:
            account = CompanyAccount("żabka", "1111111111", force_inactive=True)
        except ValueError as error:
            assert str(error) == "Company not registered!!"

    @pytest.mark.parametrize(
        "balance1,balance2,expected1,expected2",
        [(100, 100, 45, 150), (20, 0, 20, 0), (50, 0, -5, 50)],
        ids=[
            "regular_express_transfer",
            "insufficnient_balance_express",
            "transfer_all_express",
        ],
    )
    def test_express_transfer(
        self, balance1, balance2, expected1, expected2, account, account2
    ):
        account.balance = balance1
        account2.balance = balance2
        account.make_express_transfer(50, account2)
        assert account.balance == expected1 and account2.balance == expected2

    def test_account_history(self, account, account2):
        account.receive_transfer(500)
        account.make_transfer(300, account2)
        account.make_express_transfer(100, account2)
        account.make_transfer(100, account2)

        assert account.history == [500, -300, -100, -5]

    @pytest.mark.parametrize(
        "balance, history, expected",
        [
            (500, [10, -1775, -10, -1000000, 10000000000, 67], True),
            (100, [-1775], True),
            (99, [-1775], False),
            (200, [10, 10, 10, 10], False),
        ],
        ids=["normal", "exactly_twice", "insufficient_balance", "no_tax"],
    )
    def test_take_loan(self, balance, history, expected, account):
        account.balance = balance
        account.history = history
        print(account.balance, account.history)
        assert account.take_loan(50) == expected
