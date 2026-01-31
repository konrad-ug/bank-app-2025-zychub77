import os

from pymongo import MongoClient
from src.PersonalAccount import PersonalAccount
from src.AccountsRepository import AccountsRepository


class MongoAccountsRepository(AccountsRepository):
    def __init__(
        self, uri=None, db_name="bank_app", collection_name="accounts"
    ):
        mongo_uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self._client = MongoClient(mongo_uri)
        self._collection = self._client[db_name][collection_name]

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            if hasattr(account, "to_dict"):
                payload = account.to_dict()
            else:
                payload = {
                    "pesel": getattr(account, "pesel", None),
                    "balance": getattr(account, "balance", 0.0),
                    "history": getattr(account, "history", []),
                }
            self._collection.update_one(
                {"pesel": payload.get("pesel")},
                {"$set": payload},
                upsert=True,
            )

    def load_all(self):
        accounts = []
        for doc in self._collection.find({}):
            first_name = doc.get("first_name")
            last_name = doc.get("last_name")
            pesel = doc.get("pesel")
            promo_code = doc.get("promo_code", "Invalid")
            account = PersonalAccount(first_name, last_name, pesel, promo_code)
            account.balance = doc.get("balance", 0.0)
            account.history = doc.get("history", [])
            accounts.append(account)
        return accounts
