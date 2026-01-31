import re
from smtp.smtp import SMTPClient


class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []
        self.history_email_preamble = "Account history:"

    def receive_transfer(self, amount):
        self.balance += amount
        self.history.append(amount)

    def make_transfer(self, amount, transferAccount):
        if self.balance >= amount:
            self.balance -= amount
            transferAccount.receive_transfer(amount)
            self.history.append(-amount)
            return True
        return False

    def make_express_transfer(self, amount, transferAccount, fee):
        if self.balance >= amount:
            self.balance -= amount + fee
            transferAccount.receive_transfer(amount)
            self.history.append(-amount)
            self.history.append(-fee)
            return True
        return False
    
    def send_history_via_email(self, email):
        return SMTPClient.send(
            "Account history", f"{self.history_email_preamble} {self.history}", email
        )
