from functools import wraps
import web3
import time
import sys

def gas_cost(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        txn_hash = method(self, *args, **kwargs)
        gas_used = self.w3.eth.getTransactionReceipt(txn_hash)['gasUsed']
        last_block = self.w3.eth.get_block('latest')
        function_name = method.__name__
        #added 
        sizeof_input = sys.getsizeof(self.w3.eth.getTransaction(txn_hash)['input'])
        sizeof_txn = sys.getsizeof(self.w3.eth.getTransaction(txn_hash))
        block_number = self.w3.eth.getTransactionReceipt(txn_hash)['blockNumber']
        block_time = self.w3.eth.getBlock(block_number)['timestamp']
        block_cost = self.w3.eth.getBlock(block_number)['gasUsed']
        block_tx_no = len(self.w3.eth.getBlock(block_number)['transactions'])

        with open("./gas_cost/gas_cost.csv", "a") as f:
            f.write(function_name+","
                +str(block_number)+","
                +str(block_time)+","
                +str(block_cost)+","
                +str(block_tx_no)+","
                +str(gas_used)+","
                +self.private_key[0:6]+","
                +str(last_block['number'])+","
                +str(sizeof_input)+","
                +str(sizeof_txn)+"\n")

    return wrapper