#!/home/matti/IoT-Microservice/venv/bin/python3.8
# coding: utf-8

# In[1]:


import sys
from web3 import Web3


# In[2]:


def connect(settings):
    
    # WEBSOCKET ADDRESS
    address = 'ws://{}:{}'.format(settings['gateway']['host'], settings['gateway']['port'])
    
    # CREATE A WEB3 INSTANCE
    instance = Web3(Web3.WebsocketProvider(address))
    
    # CHECK INSTANCE CONNECTION
    if instance.isConnected():
        return instance
        
    # IF IT FAILS, ABORT THE PROCESS
    else:
        print('COULD NOT CONNECT TO GATEWAY!')
        sys.exit(0)


# In[3]:


class contract:
    
    # ON LOAD..
    def __init__(self, block, web3, settings):
        
        # CONSTRUCT USABLE CONTRACT
        self.contract = web3.eth.contract(
            address = block['address'],
            abi = block['abi']
        )
        
        # SET ADDRESS REFERENCE & WEB3 INSTANCE
        self.address = block['address']
        self.web3 = web3
        self.settings = settings
    
    # READ FROM CONTRACT
    def read(self, details):
        
        # WITH PARAMS
        if type(details) == dict:
            return self.contract.functions[details['func']](details['params']).call()
        
        # WITHOUT PARAMS
        elif type(details) == str:
            return self.contract.functions[details]().call()
    
    # WRITE TO CONTRACT
    def write(self, details):
        try:
            
            # CREATE BASE TRANSACTION
            tx = {
                'from': self.settings['keys']['public'],
                'to': self.contract.address,
                'data': self.contract.encodeABI(
                    fn_name = details['func'],
                    args = details['params']
                )
            }
            
            # ESTIMATE GAS VALUE & STITCH IN REMAINING PROPS
            tx['gas'] = self.web3.eth.estimateGas(tx)
            tx['gasPrice'] = self.web3.toWei(20, 'gwei')
            tx['nonce'] = self.web3.eth.getTransactionCount(self.settings['keys']['public'])

            # SIGN TRANSCTION WITH PRIVATE KEY
            signed = self.web3.eth.account.sign_transaction(tx,
                private_key = self.settings['keys']['private']
            )

            # SEND THE TRANSACTION
            tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)

            # WAIT FOR IT TO BE MINED
            return self.web3.eth.waitForTransactionReceipt(tx_hash, 500)
        
        # IF THE TRANSACTION IS REVERTED, SHOW ERROR
        except ValueError as error:
            return error
    
    # EVENT FILTER
    def event(self, name):
        return self.contract.events[name].createFilter(fromBlock='latest')

