from src.PersonalAccount import PersonalAccount


class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def getAllAccounts(self):
        return self.accounts

    def getNumberOfAccounts(self):
        return len(self.accounts)

    def addAccount(self, account):
        self.accounts.append(account)

    def getAccountByPESEL(self, PESEL):
        for account in self.accounts:
            if account.pesel == PESEL:
                return account
        return None
