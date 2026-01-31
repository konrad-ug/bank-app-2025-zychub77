from src.account import Account
import requests
import datetime
import os


BANK_APP_MF_URL = os.getenv(
    "BANK_APP_MF_URL", "https://wl-api.mf.gov.pl/api/search/nip/"
)


# force_inactive exists because it's not reasonably possible to find an inactive NIP by hand, and it could get reactivated/removed
class CompanyAccount(Account):
    def __init__(self, company_name, NIP, force_inactive=False):
        super().__init__()
        self.company_name = company_name
        self.force_inactive = force_inactive
        self.history_email_preamble = "Company account history:"
        self.NIP = self.set_NIP(NIP)
        if self.NIP == "Unregistered":
            raise ValueError("Company not registered!!")
        self.balance = 0.0

    def set_NIP(self, NIP):
        if len(NIP) != 10:
            return "Invalid"
        if not self.check_NIP(NIP):
            return "Unregistered"
        return NIP

    def make_express_transfer(self, amount, transferAccount):
        super().make_express_transfer(amount, transferAccount, 5)

    def take_loan(self, amount):
        if self.balance >= 2 * amount:
            for transaction in self.history:
                if transaction == -1775:
                    return True
        return False

    def check_NIP(self, NIP):
        mdate = datetime.date.today()
        url = f"{BANK_APP_MF_URL }{NIP}?date={mdate}"
        response = requests.get(url)

        data = response.json()["result"]
        print(data)
        if data["subject"] == None and not self.force_inactive:
            print("Konto nie istnieje")
            return False

        if self.force_inactive or data["subject"]["statusVat"] != "Czynny":
            print("Konto nieczynne")
            return False
        print("Konto czynne")
        return True

    def send_history_via_email(self, email):
        return super().send_history_via_email(email)
