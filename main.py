import requests
import math

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

def amount_transactions_at_address(address):
    url = "https://api-testnet.ergoplatform.com/api/v1/addresses/" + str(address) + "/transactions"
    data = requests.get(url).json()
    total = data["total"]
    return total

def get_transactions(address, offset):
    url = "https://api-testnet.ergoplatform.com/api/v1/addresses/" + str(address) + "/transactions?limit=500&offset=" + str(offset)
    data = requests.get(url).json()
    return data

def create_transaction_array(address, offset):
    transactionData = get_transactions(address, offset)["items"]
    transactionArray = []
    for i in transactionData:
        id = i["id"]
        inclusionHeight = i["inclusionHeight"]
        outputs = i["outputs"]
        t = Transaction(id, inclusionHeight, outputs)
        transactionArray.append(t)
    return transactionArray

def lookup_ergoname_id(transactionArray, name):
    for i in transactionArray:
        for o in i.outputs:
            for a in o.assets:
                if name == a.name:
                    return a.tokenId

def get_box_of_asset(id):
    url = TESTNET_API_URL + "/api/v1/tokens/" + str(id)
    data = requests.get(url).json()
    boxId = data["boxId"]
    return boxId

def get_box_id_address(boxId):
    url = TESTNET_API_URL + "/api/v1/boxes/" + str(boxId)
    data = requests.get(url).json()
    address = data["address"]
    return address

def reformat_name(name):
    newName = ""
    for i in name:
        if i == " ":
            newName += "%20"
        else:
            newName += i
    return newName

def resolve_ergoname(name):
    total = amount_transactions_at_address(MINT_ADDRESS)
    neededCalls = math.floor(total / 500) + 1
    offset = 0
    transactionArray = []
    for i in range(neededCalls):
        transactionArray += create_transaction_array(MINT_ADDRESS, offset)
        offset += 500

    index = 0
    for i in transactionArray:
        i.update_outputs()
        for o in transactionArray[index].outputs:
            o.update_assets()
        index += 1
    
    id = lookup_ergoname_id(transactionArray, name)
    boxId = get_box_of_asset(id)
    address = get_box_id_address(boxId)
    return address

def main():

    address = resolve_ergoname("test mint v0.1.1")
    print(address)

if __name__=="__main__":
    main()