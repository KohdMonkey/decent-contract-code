#!/usr/bin/python3.8

from web3 import Web3
import json
import time

w3 = Web3(Web3.IPCProvider(
    "/path/to/datadir/geth.ipc", timeout=60000))

'''
Source: https://stackoverflow.com/questions/49854190/how-to-get-event-data-from-web3py
'''
def handleEvent(event):
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    add = addEvent.processReceipt(receipt) 
    revocation = revocationEvent.processReceipt(receipt)

    if add:
        enclaveId = add[0]['args']['enclaveId']
        print('adding enclave: ', enclaveId)
    
    if revocation:
        enclaveId = revocation[0]['args']['enclaveId']
        print('revoking enclave: ', enclaveId)

def logLoop(blockFilter, poll_interval):
    while True:
        for event in blockFilter.get_new_entries():
            handleEvent(event)
            time.sleep(poll_interval)


# given contract addr and abi file, construct contract
contractAddress = '0x3120efa0C1a8e91425fd3B1E3EF63598D8816711'
abiFile = open('abi.json')
contractabi = json.load(abiFile)
contract = w3.eth.contract(address=contractAddress, abi=contractabi)

# filtering a block for transactions to the contract
blockFilter = w3.eth.filter({'fromBlock':'latest', 'address':contractAddress})

# contract events to listen for
addEvent = contract.events.add()
revocationEvent = contract.events.revoke()

logLoop(blockFilter, 2)
