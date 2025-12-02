from src.account import Account


class CompanyAccount(Account):
    def __init__(self, company_name, NIP):
        super().__init__()
        self.company_name = company_name
        self.NIP = NIP if self.is_NIP_valid(NIP) else "Invalid"
        self.balance = 0.0

    def is_NIP_valid(self, NIP):
        if len(NIP) != 10:
            return False
        return True

    def make_express_transfer(self, amount, transferAccount):
        super().make_express_transfer(amount, transferAccount, 5)

    def take_loan(self, amount):
        if self.balance >= 2 * amount:
            # print("Balance good")
            for transaction in self.history:
                # print("Starting loop")
                if transaction == -1775:
                    # print("Found Good transaction")
                    return True
        return False
