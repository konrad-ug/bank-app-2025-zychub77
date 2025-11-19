import re


class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []

    def receive_transfer(self, amount):
        self.balance += amount
        self.history.append(amount)

    def make_transfer(self, amount, transferAccount):
        if self.balance >= amount:
            self.balance -= amount
            transferAccount.receive_transfer(amount)
            self.history.append(-amount)

    def make_express_transfer(self, amount, transferAccount, fee):
        if self.balance >= amount:
            self.balance -= amount + fee
            transferAccount.receive_transfer(amount)
            self.history.append(-amount)
            self.history.append(-fee)

    def approve_loan(self, amount):
        if len(self.history) >= 5:
            sum = 0
            for x in self.history:
                sum += x
            if sum > amount:
                return True
        elif len(self.history) >= 3:
            for x in self.history:
                if x < 0:
                    return False
            return True
        return False

    def submit_for_loan(self, amount):
        if self.approve_loan(amount) == True:
            self.receive_transfer(amount)
            return True
        return False
