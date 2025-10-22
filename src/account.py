import re


class Account:
    def __init__(self):
        self.balance = 0.0

    def receive_transfer(self, amount):
        self.balance += amount

    def make_transfer(self, amount, transferAccount):
        if self.balance >= amount:
            self.balance -= amount
            transferAccount.receive_transfer(amount)

    def make_express_transfer(self, amount, transferAccount, fee):
        if self.balance >= amount:
            self.balance -= amount + fee
            transferAccount.receive_transfer(amount)
