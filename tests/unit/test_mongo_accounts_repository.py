from src.MongoAccountsRepository import MongoAccountsRepository
from src.PersonalAccount import PersonalAccount


def test_save_all_clears_and_upserts(mocker):
    mock_collection = mocker.Mock()
    mock_db = mocker.MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_client = mocker.MagicMock()
    mock_client.__getitem__.return_value = mock_db
    mocker.patch("src.MongoAccountsRepository.MongoClient", return_value=mock_client)

    repo = MongoAccountsRepository("mongodb://test")
    account1 = PersonalAccount("A", "B", "05280199999", "PROM_123")
    account1.balance = 10
    account1.history = [10]
    account2 = PersonalAccount("C", "D", "05280199998", "PROM_123")
    account2.balance = 20
    account2.history = [20]

    repo.save_all([account1, account2])

    mock_collection.delete_many.assert_called_once_with({})
    assert mock_collection.update_one.call_count == 2


def test_load_all_returns_accounts(mocker):
    mock_collection = mocker.Mock()
    mock_collection.find.return_value = [
        {
            "first_name": "A",
            "last_name": "B",
            "pesel": "05280199999",
            "balance": 10,
            "history": [10],
            "promo_code": "PROM_123",
        },
        {
            "first_name": "C",
            "last_name": "D",
            "pesel": "05280199998",
            "balance": 20,
            "history": [20],
            "promo_code": "PROM_123",
        },
    ]
    mock_db = mocker.MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_client = mocker.MagicMock()
    mock_client.__getitem__.return_value = mock_db
    mocker.patch("src.MongoAccountsRepository.MongoClient", return_value=mock_client)

    repo = MongoAccountsRepository("mongodb://test")
    accounts = repo.load_all()

    assert len(accounts) == 2
    assert accounts[0].first_name == "A"
    assert accounts[0].last_name == "B"
    assert accounts[0].pesel == "05280199999"
    assert accounts[0].balance == 10
    assert accounts[0].history == [10]
