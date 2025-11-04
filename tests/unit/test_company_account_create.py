from src.CompanyAccount import CompanyAccount


class TestCompanyAccount:
    def test_account_creation(self):
        account = CompanyAccount("żabka", "1234567890")
        assert account.company_name == "żabka"
        assert account.NIP == "1234567890"

    def test_account_NIP_validation(self):
        account3 = CompanyAccount("lidl", "123")
        assert account3.NIP == "Invalid"

    def test_make_express_transfer(self):
        account = CompanyAccount("żabka", "1234567890")
        account2 = CompanyAccount("biedronka", "0987654321")
        account.balance = 10
        account.make_express_transfer(10, account2)
        assert account.balance == -5.0

    def test_account_history(self):
        account = CompanyAccount("żabka", "1234567890")
        account2 = CompanyAccount("biedronka", "0987654321")
        account.receive_transfer(500)
        account.make_transfer(300, account2)
        account.make_express_transfer(100, account2)
        account.make_transfer(100, account2)

        assert account.history == [500, -300, -100, -5]
