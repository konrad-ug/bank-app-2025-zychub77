from src.PersonalAccount import PersonalAccount
import re
import pytest


class TestPersonalAccount:
    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "05280199999", "PROM_123")
        return account

    @pytest.fixture
    def account2(self):
        account2 = PersonalAccount("John", "Doe", "05280199999", "PROM_123")
        return account2

    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "05080101397", "PROM_123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "05080101397"

    @pytest.mark.parametrize(
        "PESEL,expected",
        [("05280199999", "05280199999"), ("123", "Invalid")],
        ids=["valid_pesel", "invalid_pesel"],
    )
    def test_PESEL_validation(self, PESEL, expected):
        account = PersonalAccount("John", "Doe", PESEL, "PROM_123")
        assert account.pesel == expected

    @pytest.mark.parametrize(
        "PESEL,prom,expected",
        [
            ("05280101397", "PROM_123", 50),
            ("05280101397", "PROM_12", 0),
            ("05880101397", "PROM_123", 0),
            ("05480101397", "PROM_123", 50),
            ("05480101397", "PROM_12", 0),
            ("05680101397", "PROM_123", 50),
            ("05680101397", "PROM_12", 0),
        ],
        ids=[
            "promo_2000_valid",
            "promo_200_invalid",
            "promo_1800",
            "promo_2100_valid",
            "promo_2100_invalid",
            "promo_2200_valid",
            "promo_2200_invalid",
        ],
    )
    def test_promo_validation(self, PESEL, prom, expected):
        account = PersonalAccount("John", "Doe", PESEL, prom)
        assert account.balance == expected

    @pytest.mark.parametrize(
        "balance1,balance2,expected1,expected2",
        [(100, 100, 49, 150), (20, 0, 20, 0), (50, 0, -1, 50)],
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
        account.make_transfer(350, account2)
        account.make_express_transfer(100, account2)
        account.make_transfer(100, account2)

        assert account.balance == 99
        assert account.history == [500, -350, -100, -1]

    def test_account_loan(self, account):
        assert account.submit_for_loan(100) == False
        account.history = [1, 1, 1]
        assert account.submit_for_loan(100) == True
        account.history = [1, 1, -1]
        assert account.submit_for_loan(100) == False
        account.history = [25, 25, 25, 25, 25]
        assert account.submit_for_loan(100) == True
