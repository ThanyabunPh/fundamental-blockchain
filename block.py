from datetime import datetime as dt
import hashlib
import json


class Blockchain:
    # constructor to initialize the blockchain
    def __init__(self):
        self.chain = []  # list to store block
        self.data = {
            'Name': "0000",
            'Burger': "0000",
            'OrderAmount': "0000"
        }

        # create the genesis block
        self.create_block(nonce=0, previous_hash='0', data=self.data)

    def create_block(self, nonce, previous_hash, data):  # function to create a block
        block = {
            'index': len(self.chain) + 1,  # index of the block
            'timestamp': str(dt.now()),  # timestamp of the block
            'nonce': nonce,  # nonce of the block
            'previous_hash': previous_hash,  # previous hash of the block
            'data': {
                'Name': data['Name'],
                'Burger': data['Burger'],
                'OrderAmount': data['OrderAmount']
            }  # data of the block
        }

        self.chain.append(block)  # append the block to the chain
        return block  # return the block

    def get_previous_block(self):  # function to get the previous block
        return self.chain[-1]  # return the last block of the chain

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce ** 2 - previous_nonce ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1

        return new_nonce
