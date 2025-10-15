from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "09359462739")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert len(account.pesel) == 11
        assert len(account.pesel) == 11
