from src.account import Account
import re


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "09359462739", "PROM_123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "09359462739"
        assert len(account.pesel) == 11 or account.pesel == "Invalid"
        assert account.promo_code == "PROM_123"
        assert re.search("^PROM_.{3}$",account.promo_code) != None or account.promo_code is None
