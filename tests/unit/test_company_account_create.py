from src.CompanyAccount import CompanyAccount


class TestCompanyAccount:
    def test_account_creation(self):
        account = CompanyAccount("żabka", "1234567890")
        assert account.company_name == "żabka"
        assert account.NIP == "1234567890"

    def test_account_make_transfer(self):
        account = CompanyAccount("żabka", "1234567890")
        account2 = CompanyAccount("biedronka", "1234567890")
        account.balance = 100.0
        account2.balance = 200.0
        firstBalance = account.balance + account2.balance
        account.make_transfer(50.0, account2)
        assert firstBalance == account.balance + account2.balance

    def test_account_NIP_validation(self):
        account3 = CompanyAccount("lidl", "123")
        assert account3.NIP == "Invalid"

    def test_account_express_transfer(self):
        account = CompanyAccount("żabka", "1234567890")
        account2 = CompanyAccount("biedronka", "1234567890")
        account.balance = 10.0
        account2.balance = 0.0
        account.make_express_transfer(10.0, account2)
        assert account.balance == -5.0
