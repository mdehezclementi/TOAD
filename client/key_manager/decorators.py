from functools import wraps
import web3
import time
import sys

def member_required(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not(self.is_member):
            raise ValueError("you have not proved you are a group member")
        return method(self, *args, **kwargs)
    return wrapper

def gas_cost(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        txn_hash = method(self, *args, **kwargs)
        sizeof_input = sys.getsizeof(self.w3.eth.getTransaction(txn_hash)['input'])
        sizeof_txn = sys.getsizeof(self.w3.eth.getTransaction(txn_hash))
        #status = self.w3.eth.getTransactionReceipt(txn_hash)['status']
        block_number = self.w3.eth.getTransactionReceipt(txn_hash)['blockNumber']
        block_time = self.w3.eth.getBlock(block_number)['timestamp']
        block_cost = self.w3.eth.getBlock(block_number)['gasUsed']
        block_tx_no = len(self.w3.eth.getBlock(block_number)['transactions'])
        gas_used = self.w3.eth.getTransactionReceipt(txn_hash)['gasUsed']

        # index = 0 
        # thereIsData = True 
        # storage_at_contract = b""
        # while thereIsData :
        #     try :
        #         storage_at_contract+=self.w3.eth.getStorageAt("0x5b1869D9A4C187F2EAa108f3062412ecf0526b24",index)
        #         index += 1
        #         if index == 20:
        #             thereIsData =False
        #     except Exception as e:
        #         thereIsData = False
        #storage_at_contract=self.w3.eth.getStorageAt("0x5b1869d9a4c187f2eaa108f3062412ecf0526b24",0)


        last_block = self.w3.eth.get_block('latest')
        function_name = method.__name__
        
        with open("../gas_cost/gas_cost.csv", "a") as f:
            f.write(function_name+","
                +str(block_number)+","
                +str(block_time)+","
                +str(block_cost)+","
                +str(block_tx_no)+","
                #+str(status)+","
                +str(gas_used)+","
                +self.private_key[0:6]+","
                #+str(storage_at_contract)+","
                #+str(sys.getsizeof(storage_at_contract))+","
                +str(last_block['number'])+","
                +str(sizeof_input)+","
                +str(sizeof_txn)+"\n")
                

    return wrapper
