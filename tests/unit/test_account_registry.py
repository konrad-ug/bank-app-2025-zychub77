from src.AccountRegistry import AccountRegistry
from src.PersonalAccount import PersonalAccount
import pytest


class TestAccountRegistry:
    @pytest.fixture
    def registry(self):
        registry = AccountRegistry()
        return registry

    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "05280199999", "PROM_123")
        return account

    @pytest.fixture
    def fullRegistry(self):
        fullRegistry = AccountRegistry()
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "04280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "02280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "01280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "06280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "08280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "09280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "15280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "25280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "35280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "45280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "55280199999", "PROM_123")
        )
        fullRegistry.addAccount(
            PersonalAccount("John", "Doe", "65280199999", "PROM_123")
        )
        return fullRegistry

    def test_registry_creation(self, registry):
        assert registry.accounts == []

    def test_registry_add_account(self, registry, account):
        registry.addAccount(account)
        assert registry.accounts[0] == account

    def test_registry_get_account_by_PESEL(self, fullRegistry):
        assert fullRegistry.getAccountByPESEL("15280199999").pesel == "15280199999"

    def test_registry_get_account_by_PESEL_not_found(self, fullRegistry):
        assert fullRegistry.getAccountByPESEL("1") is None

    def test_registry_get_number_of_accounts(self, fullRegistry):
        assert fullRegistry.getNumberOfAccounts() == 12

    def test_registry_get_all_accounts(self, fullRegistry):
        assert fullRegistry.getAllAccounts() == fullRegistry.accounts
