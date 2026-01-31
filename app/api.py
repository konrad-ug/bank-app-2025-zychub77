from src.AccountRegistry import AccountRegistry
from src.PersonalAccount import PersonalAccount
from src.MongoAccountsRepository import MongoAccountsRepository
from flask import Flask, request, jsonify


app = Flask(__name__)
registry = AccountRegistry()
accounts_repository = MongoAccountsRepository()


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    accounts_data = registry.getAllAccounts()
    if any(account.pesel == data["pesel"] for account in accounts_data):
        return jsonify({"message": "An account with this PESEL already exists"}), 409
    else:
        account = PersonalAccount(data["name"], data["last_name"], data["pesel"])
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


@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def make_transfer_by_pesel(pesel):
    data = request.get_json()
    account = registry.getAccountByPESEL(pesel)
    if account is None:
        return jsonify({"message": "No account found"}), 404
    if data["type"] == "incoming":
        account.receive_transfer(data["amount"])
        return jsonify({"message": "Transfer received"}), 200

    outgoing_account = registry.getAccountByPESEL(data["outgoing_pesel"])
    if outgoing_account is None:
        return jsonify({"message": "No account found"}), 404

    transfer_success = account.make_transfer(data["amount"], outgoing_account)
    if not transfer_success:
        return jsonify({"message": "Transfer failed"}), 200

    return jsonify({"message": "Transfer completed successfully"}), 200


@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def update_account(pesel):
    account = registry.getAccountByPESEL(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json() or {}
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    if "last_name" in data:
        account.last_name = data["last_name"]
    return jsonify({"message": "Account updated"}), 200


@app.route("/api/accounts/<pesel>", methods=["DELETE"])
def delete_account(pesel):
    accounts_data = list(registry.getAllAccounts())
    registry.accounts = [
        account for account in accounts_data if account.pesel != pesel
    ]
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/accounts/save", methods=["POST"])
def save_accounts():
    accounts_repository.save_all(registry.getAllAccounts())
    return jsonify({"message": "Accounts saved"}), 200


@app.route("/api/accounts/load", methods=["POST"])
def load_accounts():
    registry.accounts = accounts_repository.load_all()
    return jsonify({"message": "Accounts loaded"}), 200
