from src.PersonalAccount import PersonalAccount
import re


class TestPersonalAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "05080101397", "PROM_123")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "05080101397"

    def test_PESEL_validation(self):
        account = PersonalAccount("John", "Doe", "05080101397", "PROM_123")
        assert len(account.pesel) == 11 or account.pesel == "Invalid"

    def test_promo_validation(self):
        account = PersonalAccount("John", "Doe", "05080101397", "PROM_123")
        print(account.promo_code)
        print(account.destruct_pesel())
        assert account.promo_code == "PROM_123" or account.destruct_pesel()[2] <= 1960
        assert (
            re.search("^PROM_.{3}$", account.promo_code) != None
            or account.promo_code == "Invalid"
        )
