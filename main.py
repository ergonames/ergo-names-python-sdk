import requests
import math
import time

TESTNET_API_URL = "https://api-testnet.ergoplatform.com/"
MAINNET_API_URL = "https://api.ergoplatform.com/"

MINT_ADDRESS = "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"

class Transaction:

    def __init__(self, id, inclusionHeight, outputs):
        self.id = id
        self.inclusionHeight = inclusionHeight
        self.outputs = outputs

    def update_outputs(self):
        outputArray = []
        for i in self.outputs:
            assets = i["assets"]
            opt = Output(assets)
            outputArray.append(opt)
        self.outputs = outputArray


class Output:

    def __init__(self, assets):
        self.assets = assets

    def update_assets(self):
        assetArray = []
        for i in self.assets:
            id = i["tokenId"]
            name = i["name"]
            asset = Asset(id, name)
            assetArray.append(asset)
        self.assets = assetArray


class Asset:

    def __init__(self, tokenId, name):
        self.tokenId = tokenId
        self.name = name

def get_total_transactions_of_mint_address(address):
    url = TESTNET_API_URL + "api/v1/addresses/" + str(address) + "/transactions"
    data = requests.get(url).json()
    total = data["total"]
    return total

def get_raw_transaction_data(address, offset):
    url = TESTNET_API_URL + "api/v1/addresses/" + str(address) + "/transactions?limit=500&offset=" + str(offset)
    data = requests.get(url).json()
    return data

def create_small_transaction_array(address, offset):
    transactionData = get_raw_transaction_data(address, offset)["items"]
    transactionArray = []
    for i in transactionData:
        id = i["id"]
        inclusionHeight = i["inclusionHeight"]
        outputs = i["outputs"]
        t = Transaction(id, inclusionHeight, outputs)
        transactionArray.append(t)
    return transactionArray

def create_complete_transaction_array():
    total = get_total_transactions_of_mint_address(MINT_ADDRESS)
    neededCalls = math.floor(total / 500) + 1
    offset = 0
    transactionArray = []
    for i in range(neededCalls):
        transactionArray += create_small_transaction_array(MINT_ADDRESS, offset)
        offset += 500
    return transactionArray

def update_transaction_array(transactionArray):
    index = 0
    for tx in transactionArray:
        tx.update_outputs()
        for opt in transactionArray[index].outputs:
            opt.update_assets()
        index += 1
    return transactionArray

def get_asset_id(transactionArray, name):
    exists = False
    id = ""
    for i in transactionArray:
        for o in i.outputs:
            if check_if_transaction_mints_token():
                for a in o.assets:
                    if name == a.name:
                        exists = True
                        id = a.tokenId
                        break
    
    if exists:
        return id
    else:
        return None

def get_box_id_of_asset(id):
    if id != None:
        url = TESTNET_API_URL + "/api/v1/tokens/" + str(id)
        data = requests.get(url).json()
        boxId = data["boxId"]
        return boxId
    else:
        return None

def get_box_id_address(boxId):
    if boxId != None:
        url = TESTNET_API_URL + "/api/v1/boxes/" + str(boxId)
        data = requests.get(url).json()
        address = data["address"]
        return address
    else:
        return None

def check_if_transaction_mints_token():
    return True

def resolve_ergoname(name):
    transactionArray = create_complete_transaction_array()
    transactionArray = update_transaction_array(transactionArray)
    id = get_asset_id(transactionArray, name)
    boxId = get_box_id_of_asset(id)
    address = get_box_id_address(boxId)
    return address

def main():

    start_time = time.time()

    address = resolve_ergoname("test mint v0.1.1")
    print(address)

    print("\nProgram takes " + str(time.time() - start_time) + " seconds to run")

if __name__=="__main__":
    main()