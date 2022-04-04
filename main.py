import requests

TESTNET_API_URL = "https://api-testnet.ergoplatform.com/"
MAINNET_API_URL = "https://api.ergoplatform.com/"

def reformat_name(name):
    newName = ""
    for i in name:
        if i == " ":
            newName += "%20"
        else:
            newName += i
    return newName

def request_data(name):
    url = TESTNET_API_URL + "api/v1/tokens/search?query=" + str(name)
    data = requests.get(url).json()
    return data

def get_token_id(name):
    data = request_data(name)
    id = data["items"][0]["id"]
    return id

def get_token_box_id(id):
    url = TESTNET_API_URL + "/api/v1/tokens/" + str(id)
    data = requests.get(url).json()
    boxId = data["boxId"]
    return boxId

def get_box_id_address(id):
    url = TESTNET_API_URL + "/api/v1/boxes/" + str(id)
    data = requests.get(url).json()
    address = data["address"]
    return address

def resolve_ergo_name(name):
    name = reformat_name(name)
    id = get_token_id(name)
    boxId = get_token_box_id(id)
    address = get_box_id_address(boxId)
    return address

# def main():

#     name = "test mint v0.1.1"
#     address = resolve_ergo_name(name)
#     print(address)

# if __name__=="__main__":
#     main()