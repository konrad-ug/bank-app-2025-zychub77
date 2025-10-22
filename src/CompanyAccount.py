class CompanyAccount:
    def __init__(self, company_name, NIP):
        self.company_name = company_name
        self.NIP = NIP if self.is_NIP_valid(NIP) else "Invalid"
        self.balance = 0.0

    def is_NIP_valid(self, NIP):
        if len(NIP) != 10:
            return False
        return True

    def receive_transfer(self, amount):
        self.balance += amount

    def make_transfer(self, amount, transferAccount):
        if self.balance >= amount:
            self.balance -= amount
            transferAccount.receive_transfer(amount)

    def make_express_transfer(self, amount, transferAccount):
        if self.balance >= amount:
            self.balance -= amount + 5
            transferAccount.receive_transfer(amount)
