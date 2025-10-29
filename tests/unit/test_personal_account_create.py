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

    def test_PESEL_invalid(self):
        account = PersonalAccount("John", "Doe", "123", "PROM_123")
        assert account.pesel == "Invalid"

    def test_promo_validation_2000(self):
        account = PersonalAccount("John", "Doe", "05280101397", "PROM_123")
        assert account.promo_code == "PROM_123"
        assert re.search("^PROM_.{3}$", account.promo_code) != None

    def test_promo_validation_1800(self):
        account = PersonalAccount("John", "Doe", "05880101397", "PROM_123")
        assert account.promo_code == "Invalid"

    def test_promo_validation_2100(self):
        account = PersonalAccount("John", "Doe", "05480101397", "PROM_123")
        assert account.balance == 50.0
        account = PersonalAccount("John", "Doe", "05480101397", "PROM_12")
        assert account.balance == 0.0

    def test_promo_validation_2200(self):
        account = PersonalAccount("John", "Doe", "05680101397", "PROM_123")
        assert account.balance == 50.0
        account = PersonalAccount("John", "Doe", "05680101397", "PRRASDAS")
        assert account.balance == 0.0

    def test_make_express_transfer(self):
        account = PersonalAccount("John", "Doe", "05280101397", "PROM_123")
        account2 = PersonalAccount("Jane", "Doe", "05280101397", "PROM_123")
        account.balance = 10.1
        account.make_express_transfer(10.1, account2)
        assert account.balance == -1.0
