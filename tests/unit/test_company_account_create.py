from src.CompanyAccount import CompanyAccount
import pytest


class TestCompanyAccount:
    @pytest.fixture
    def account(self):
        account = CompanyAccount("żabka", "1234567890")
        return account

    @pytest.fixture
    def account2(self):
        account2 = CompanyAccount("biedronka", "0987654321")
        return account2

    def test_account_creation(self, account):
        assert account.company_name == "żabka"
        assert account.NIP == "1234567890"

    def test_account_NIP_validation(self):
        account3 = CompanyAccount("lidl", "123")
        assert account3.NIP == "Invalid"

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
