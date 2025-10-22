import re


class Account:
    def __init__(self, first_name, last_name, pesel, promo_code):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0 and self.init_balance()
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.promo_code = (
            promo_code if self.is_promo_code_valid(promo_code) else "Invalid"
        )

    def is_pesel_valid(self, pesel):
        if pesel and len(pesel) != 11:
            return False
        return True

    def is_promo_code_valid(self, promo_code):
        if re.search("^PROM_.{3}$", promo_code) is None:
            return False
        if self.destruct_pesel()[2] <= 1960:
            return False
        return True

    def init_balance(self):
        if self.promo_code is not None:
            self.promo_code += 50

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

    def receive_transfer(self, amount):
        self.balance += amount

    def make_transfer(self, amount, transferAccount):
        if self.balance >= amount:
            self.balance -= amount
            transferAccount.receive_transfer(amount)

    def make_express_transfer(self, amount, transferAccount):
        if self.balance >= amount:
            self.balance -= amount + 1
            transferAccount.receive_transfer(amount)
