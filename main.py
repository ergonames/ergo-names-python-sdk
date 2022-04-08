import requests
import time
import math

EXPLORER_API_URL = "https://api-testnet.ergoplatform.com/"

MINT_ADDRESS = "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"

API_CALLS = 0

class Token:

    def __init__(self, id, boxId, name):
        self.id = id
        self.boxId = boxId
        self.name = name

def get_token_data(tokenName, limit, offset):
    global API_CALLS
    url = EXPLORER_API_URL + "api/v1/tokens/search?query=" + str(tokenName) + "&limit=" + str(limit) + "&offset=" + str(offset)
    print(url)
    API_CALLS += 1
    data = requests.get(url).json()
    return data

def create_token_data(tokenName):
    total = get_token_data(tokenName, 1, 0)['total']
    neededCalls = math.floor(total / 500) + 1
    tokenData = []
    offset = 0
    for i in range(neededCalls):
        data = get_token_data(tokenName, 500, offset)['items']
        tokenData += data
    return tokenData

def convert_data_to_token(data):
    tokenArray = []
    for i in data:
        tk = Token(i['id'], i['boxId'], i['name'])
        tokenArray.append(tk)
    return tokenArray

def get_box_address(boxId):
    global API_CALLS
    url = EXPLORER_API_URL + "api/v1/boxes/" + (str(boxId))
    print(url)
    API_CALLS += 1
    data = requests.get(url).json()
    return data['address']

def check_box_address(address):
    if address == MINT_ADDRESS:
        return True
    return False

def get_asset_minted_at_address(tokenArray):
    for i in tokenArray:
        address = get_box_address(i.boxId)
        if (check_box_address(address)):
            return i.id
    return None

def get_token_transactions_data(tokenId):
    global API_CALLS
    url = EXPLORER_API_URL + "api/v1/assets/search/byTokenId?query=" + str(tokenId)
    print(url)
    API_CALLS += 1
    data = requests.get(url).json()['items']
    return data

def get_last_transaction(data):
    length = len(data)
    return data[length-1]

def get_boxid_from_transaction_data(data):
    return data['boxId']

def resolve_ergoname(name):
    name = reformat_name_search(name)
    tokenData = create_token_data(name)
    tokenArray = convert_data_to_token(tokenData)
    tokenId = get_asset_minted_at_address(tokenArray)
    tokenTransactions = get_token_transactions_data(tokenId)
    tokenLastTransaction = get_last_transaction(tokenTransactions)
    tokenCurrentBoxId = get_boxid_from_transaction_data(tokenLastTransaction)
    address = get_box_address(tokenCurrentBoxId)
    return address

def reformat_name_search(name):
    new = ""
    for i in name:
        if i == " ":
            new += "%20"
        else:
            new += i
    return new

def main():

    start_time = time.time()

    address = resolve_ergoname("test mint v0.1.1")
    print("\nResolved Address: " + address)
    print("Mint Address: " + MINT_ADDRESS)

    print("\nExplorer calls: " + str(API_CALLS))
    print("Program time: " + str(time.time() - start_time))

if __name__=="__main__":
    main()