from behave import *
import requests

URL = "http://localhost:5000"


@step(
    'I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"'
)
def create_account(context, name, last_name, pesel):
    json_body = {
        "name": f"{name}",
        "last_name": f"{last_name}",
        "pesel": pesel,
    }
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201


@step("Account registry is empty")
@step("Accoount registry is empty")
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")


@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert response.status_code == 200
    assert response.json()["count"] == int(count)


@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()["pesel"] == pesel


@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()["pesel"] is None


@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200


@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    if field == "surname":
        json_body = {"last_name": f"{value}"}
    else:
        json_body = {"name": f"{value}"}
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200


@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    data = response.json()
    if field == "name":
        assert data.get("first_name") == value
    elif field == "surname":
        assert data.get("last_name") == value or data.get("surname") == value
    elif field == "pesel":
        assert data["pesel"] == value
    else:
        raise ValueError(f"Invalid field: {field}.")


@when('I make incoming transfer of "{amount}" to account with pesel: "{pesel}"')
def incoming_transfer(context, amount, pesel):
    response = requests.post(
        URL + f"/api/accounts/{pesel}/transfer",
        json={"type": "incoming", "outgoing_pesel": None, "amount": float(amount)},
    )
    assert response.status_code == 200


@when(
    'I make outgoing transfer of "{amount}" from account with pesel: "{pesel}" to account with pesel: "{outgoing_pesel}"'
)
def outgoing_transfer(context, amount, pesel, outgoing_pesel):
    response = requests.post(
        URL + f"/api/accounts/{pesel}/transfer",
        json={
            "type": "outgoing",
            "outgoing_pesel": outgoing_pesel,
            "amount": float(amount),
        },
    )
    assert response.status_code == 200


@then('Account with pesel "{pesel}" has balance equal to "{balance}"')
def account_balance_equals(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()["balance"] == float(balance)
