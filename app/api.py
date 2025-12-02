from src.AccountRegistry import AccountRegistry
from src.PersonalAccount import PersonalAccount
from flask import Flask, request, jsonify


app = Flask(__name__)
registry = AccountRegistry()


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.addAccount(account)
    return jsonify({"message": "Account created"}), 201


@app.route("/api/accounts", methods=["GET"])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.getAllAccounts()
    accounts_data = [
        {
            "name": acc.first_name,
            "surname": acc.last_name,
            "pesel": acc.pesel,
            "balance": acc.balance,
        }
        for acc in accounts
    ]
    return jsonify(accounts_data), 200


@app.route("/api/accounts/count", methods=["GET"])
def get_account_count():
    print("Get account count request received")
    count = registry.getNumberOfAccounts()

    return jsonify({"count": count}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def get_account_by_pesel(pesel):
    account = registry.getAccountByPESEL(pesel)
    if account is not None:
        account_data = {
            "first_name": account.first_name,
            "last_name": account.last_name,
            "pesel": account.pesel,
            "balance": account.balance,
        }
    else:
        account_data = {
            "first_name": None,
            "last_name": None,
            "pesel": None,
            "balance": None,
        }

    return jsonify(account_data), 200


@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def update_account(pesel):
    account = registry.getAccountByPESEL(pesel)
    if account is not None:
        account.pesel = pesel
    return jsonify({"message": "Account updated"}), 200


@app.route("/api/accounts/<pesel>", methods=["DELETE"])
def delete_account(pesel):
    accounts_data = registry.getAllAccounts()
    registry.accounts = filter(lambda account: account.pesel != pesel, accounts_data)
    return jsonify({"message": "Account deleted"}), 200
