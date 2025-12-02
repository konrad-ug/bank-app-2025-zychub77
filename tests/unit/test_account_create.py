from src.account import Account
import pytest


class TestAccount:
    @pytest.fixture
    def account(self):
        account = Account()
        return account

    @pytest.fixture
    def account2(self):
        account2 = Account()
        return account2

    def test_account_creation(self, account):
        account = Account()
        assert account.balance == 0.0

    @pytest.mark.parametrize(
        "balance1,balance2,expected1,expected2",
        [(100, 2000, 50, 2050), (10, 0, 10, 0), (50, 0, 0, 50)],
        ids=["regular_transfer", "insufficnient_balance", "transfer_all"],
    )
    def test_transfer(
        self, balance1, balance2, expected1, expected2, account, account2
    ):
        account.balance = balance1
        account2.balance = balance2
        account.make_transfer(50.0, account2)
        assert account.balance == expected1 and account2.balance == expected2

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
        account.make_express_transfer(50, account2, 5)
        assert account.balance == expected1 and account2.balance == expected2

    def test_account_history(self, account, account2):
        account.receive_transfer(500)
        account.make_transfer(300, account2)
        account.make_express_transfer(100, account2, 1)
        account.make_transfer(100, account2)

        assert account.history == [500, -300, -100, -1]
