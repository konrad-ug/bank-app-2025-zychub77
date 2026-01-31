import re
from src.account import Account


class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code="Invalid"):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.history_email_preamble = "Personal account history:"
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.promo_code = (
            promo_code if self.is_promo_code_valid(promo_code) else "Invalid"
        )
        self.init_balance()

    def is_pesel_valid(self, pesel):
        if pesel and len(pesel) != 11:
            return False
        return True

    def is_promo_code_valid(self, promo_code):
        if re.search("^PROM_.{3}$", promo_code) is None:
            return False
        if self.pesel == "Invalid" or self.destruct_pesel()[2] <= 1960:
            return False
        return True

    def init_balance(self):
        if self.is_promo_code_valid(self.promo_code):
            self.balance += 50

    def destruct_pesel(self):
        coded_month = int(self.pesel[2:4])
        year_of_century = int(self.pesel[0:2])
        day = int(self.pesel[4:6])
        if coded_month > 80:
            year = 1800 + year_of_century
            month = coded_month - 80
        elif coded_month > 60:
            year = 2200 + year_of_century
            month = coded_month - 60
        elif coded_month > 40:
            year = 2100 + year_of_century
            month = coded_month - 40
        elif coded_month > 20:
            year = 2000 + year_of_century
            month = coded_month - 20
        else:
            year = 1900 + year_of_century
            month = coded_month
        return [day, month, year]

    def make_express_transfer(self, amount, transferAccount):
        super().make_express_transfer(amount, transferAccount, 1)

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

    def send_history_via_email(self, email):
        return super().send_history_via_email(email)
