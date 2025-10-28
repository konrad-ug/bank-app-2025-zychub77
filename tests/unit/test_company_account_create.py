from src.CompanyAccount import CompanyAccount


class TestCompanyAccount:
    def test_account_creation(self):
        account = CompanyAccount("żabka", "1234567890")
        assert account.company_name == "żabka"
        assert account.NIP == "1234567890"

    def test_account_NIP_validation(self):
        account3 = CompanyAccount("lidl", "123")
        assert account3.NIP == "Invalid"
