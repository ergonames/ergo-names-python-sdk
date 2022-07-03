from ergonames.ergonames import *
import datetime

def test_resolve_ergoname():
    name = "~balb"
    assert resolve_ergoname(name) == "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"

def test_check_name_valid():
    name = "~balb"
    assert check_name_valid(name) == True

def test_check_name_price():
    name = "~balb"
    assert check_name_price(name) == None

def test_check_already_registered():
    name = "~balb"
    assert check_already_registered(name) == True

def test_get_block_id_registered():
    name = "~balb"
    assert get_block_id_registered(name) == "155b44501f6f45976623ad5b01f207434daef86a35b5efdec36cde70ef55f3c6"

def test_get_block_registered():
    name = "~balb"
    assert get_block_registered(name) == 205710

def test_get_timestamp_registered():
    name = "~balb"
    assert get_timestamp_registered(name) == 1650222939771

def test_get_date_registered():
    name = "~balb"
    timestamp = 1650222939771
    date = datetime.datetime.fromtimestamp(timestamp/1000.0)
    assert get_date_registered(name) == date

def test_get_total_amount_owned():
    address = "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"
    assert get_total_amount_owned(address) == 1

def test_reverse_search():
    address = "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"
    assert reverse_search(address) == ["~balb"]

if __name__ == "__main__":
    test_resolve_ergoname()
    test_check_name_valid()
    test_check_name_price()
    test_check_already_registered()
    test_get_block_id_registered()
    test_get_block_registered()
    test_get_timestamp_registered()
    test_get_date_registered()
    test_get_total_amount_owned()
    test_reverse_search()
    print("All tests passed")
