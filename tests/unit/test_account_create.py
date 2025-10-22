from src.account import Account
import re


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "05080101397", "PROM_123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "05080101397"
        assert len(account.pesel) == 11 or account.pesel == "Invalid"
        print(account.promo_code)
        print(account.destruct_pesel())
        assert account.promo_code == "PROM_123" or account.destruct_pesel()[2] <= 1960
        assert (
            re.search("^PROM_.{3}$", account.promo_code) != None
            or account.promo_code == "Invalid"
        )

        account2 = Account("Jane", "Doe", "55020266789", "PROM_123")
        firstBalance = account.balance + account2.balance
        account.make_transfer(50, account2)
        secondBalance = account.balance + account2.balance
        assert firstBalance == secondBalance
