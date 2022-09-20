from web3 import Web3
import os
from dotenv import load_dotenv
import time, json, requests

from web3.logs import DISCARD
load_dotenv()

os.environ['WEB3_INFURA_PROJECT_ID'] = "b4f27e1a996d427ebdaae8f9f584c74b"
web3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/b4f27e1a996d427ebdaae8f9f584c74b"))
contractAddress = '0x14A9af4FB4b24f9fcDD129D88324c1D69f9767Dc'


with open("abi.json", 'r') as j:
     contents = json.loads(j.read())
contract = web3.eth.contract(address=contractAddress, abi=contents["abi"])

mintRole_Event = contract.events.mintRole() # Modification



def update_data(discordId, tokenId):
    url = "http://127.0.0.1:8000/api/roles"

    response = json.loads(requests.get(url).text)
    for r in response:
        if r['discord']==discordId:
            if r['tokenId'] == tokenId:
                return
    payload = json.dumps({
    "products": [
        {
        "discord": discordId,
        "tokenId": tokenId
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    

def handle_event(event):
    receipt = web3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = mintRole_Event.processReceipt(receipt, errors=DISCARD)
    print(result[0]['args']._discord)
    update_data(result[0]['args']._discord, result[0]['args']._id)

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

block_filter = web3.eth.filter({'fromBlock':'latest', 'address':contractAddress})
log_loop(block_filter, 2)

