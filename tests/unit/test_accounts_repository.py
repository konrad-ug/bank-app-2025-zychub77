import pytest

from src.AccountsRepository import AccountsRepository


def test_accounts_repository_save_all_not_implemented():
    repo = AccountsRepository()
    with pytest.raises(NotImplementedError):
        repo.save_all([])


def test_accounts_repository_load_all_not_implemented():
    repo = AccountsRepository()
    with pytest.raises(NotImplementedError):
        repo.load_all()
