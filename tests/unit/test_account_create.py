from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account()
        assert account.balance == 0.0

    def test_account_make_transfer(self):
        account = Account()
        account2 = Account()

        account.balance = 100
        account2.balance = 2000
        firstBalance = account.balance + account2.balance
        account.make_transfer(50.0, account2)
        secondBalance = account.balance + account2.balance
        assert firstBalance == secondBalance

    def test_account_insufficient_balance(self):
        account = Account()
        account2 = Account()

        account.balance = 10
        account.make_transfer(20.0, account2)
        assert account.balance == 10

    def test_account_make_express_transfer(self):
        account = Account()
        account2 = Account()

        account.balance = 10.0
        account2.balance = 0.0
        account.make_express_transfer(10.0, account2, 1.0)
        assert account.balance == -1.0

    def test_account_history(self):
        account = Account()
        account2 = Account()
        account.receive_transfer(500)
        account.make_transfer(300, account2)
        account.make_express_transfer(100, account2, 1)
        account.make_transfer(100, account2)

        assert account.history == [500, -300, -100, -1]

    def test_account_load(self):
        account = Account()
        assert account.submit_for_loan(100) == False
        account.history = [1, 1, 1]
        assert account.submit_for_loan(100) == True
        account.history = [1, 1, -1]
        assert account.submit_for_loan(100) == False
        account.history = [25, 25, 25, 25, 25]
        assert account.submit_for_loan(100) == True
