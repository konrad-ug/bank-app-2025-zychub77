import os
import time

import pytest
import requests


BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
TIMEOUT_SECONDS = 0.5
MAX_RESPONSE_SECONDS = 0.5


def _assert_fast_response(response, start_time):
    elapsed = time.perf_counter() - start_time
    assert response.status_code < 500
    assert elapsed < MAX_RESPONSE_SECONDS


def _pesel_for_index(seed, index):
    value = (seed + index) % 10**11
    return f"{value:011d}"


def test_create_and_delete_account_100_times():
    seed = int(time.time() * 1000) % 10**11
    for i in range(100):
        pesel = _pesel_for_index(seed, i)
        start = time.perf_counter()
        response = requests.post(
            f"{BASE_URL}/api/accounts",
            json={"name": "Perf", "last_name": "Test", "pesel": pesel},
            timeout=TIMEOUT_SECONDS,
        )
        _assert_fast_response(response, start)
        assert response.status_code == 201

        start = time.perf_counter()
        response = requests.delete(
            f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT_SECONDS
        )
        _assert_fast_response(response, start)
        assert response.status_code == 200


def test_create_account_and_post_100_incoming_transfers():
    seed = int(time.time() * 1000) % 10**11
    pesel = _pesel_for_index(seed, 0)

    start = time.perf_counter()
    response = requests.post(
        f"{BASE_URL}/api/accounts",
        json={"name": "Perf", "last_name": "Transfers", "pesel": pesel},
        timeout=TIMEOUT_SECONDS,
    )
    _assert_fast_response(response, start)
    assert response.status_code == 201

    for _ in range(100):
        start = time.perf_counter()
        response = requests.post(
            f"{BASE_URL}/api/accounts/{pesel}/transfer",
            json={"type": "incoming", "outgoing_pesel": None, "amount": 10},
            timeout=TIMEOUT_SECONDS,
        )
        _assert_fast_response(response, start)
        assert response.status_code == 200

    start = time.perf_counter()
    response = requests.get(
        f"{BASE_URL}/api/accounts/{pesel}", timeout=TIMEOUT_SECONDS
    )
    _assert_fast_response(response, start)
    assert response.status_code == 200
    assert response.json()["balance"] == 1000
