from web3 import Web3
from eth_account import Account
import time

def wait_for_transaction_receipt(web3, txn_hash, timeout=120):
   
    #txn_hash = Web3.to_bytes(hexstr=txn_hash)
    start_time = time.time()
        
    while True:
        try:
            receipt = web3.eth.get_transaction_receipt(txn_hash)
        
            if receipt:
                if receipt.status == 1:
                    return receipt
        
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                raise TimeoutError("Thời gian chờ giao dịch đã hết. Giao dịch không hoàn thành.")
        
            time.sleep(1) 
        except :
            pass
         
'''
def bsc_sendToken(seed, address, tokenAddress):
    # Kết nối tới nút BSC (ví dụ: BSC Mainnet)
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    # Kiểm tra kết nối
    #if not web3.isConnected():
     #   raise ConnectionError("Không thể kết nối tới BSC")
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(seed)

    token_contract_address = Web3.to_checksum_address(tokenAddress)

    # ABI cơ bản cho ERC-20 (hàm `transfer`)
    erc20_abi = [
        {
            "constant": False,
            "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        }
    ]

    # Tạo đối tượng contract
    token_contract = web3.eth.contract(address=token_contract_address, abi=erc20_abi)

    # Lấy số dư token của ví
    balance = token_contract.functions.balanceOf(account.address).call()
    if balance == 0:
        raise ValueError("Không có đủ số dư để thực hiện giao dịch")

    # Sử dụng toàn bộ số dư để chuyển
    amount = balance

    # Tạo giao dịch chuyển token
    transaction = token_contract.functions.transfer(address, amount).build_transaction({
        'gas': 200000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account.address),
        'chainId': 56  # Chain ID của BSC Mainnet
    })



   
    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)

    # Gửi giao dịch
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    # In ra mã hash của giao dịch
    try:
        receipt = wait_for_transaction_receipt(web3, txn_hash)
    except TimeoutError as e:
        print(str(e))

def bsc_sendBnb(seed, recipient_address):
    # Kết nối tới nút BSC (ví dụ: BSC Mainnet)
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    # Kiểm tra kết nối
    if not web3.is_connected():
        raise ConnectionError("Không thể kết nối tới BSC")

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(seed)

    # Lấy số dư BNB của ví
    balance = web3.eth.get_balance(account.address)
    gas_estimate = 21000  # Số gas tiêu chuẩn cho giao dịch BNB
    gas_price = web3.eth.gas_price
    gas_cost = gas_estimate * gas_price

    # Số dư khả dụng để gửi (trừ phí gas)
    amount = balance - gas_cost

    if amount <= 0:
        raise ValueError("Số dư không đủ để thanh toán phí gas.")

    transaction = {
        'to': Web3.to_checksum_address(recipient_address),
        'value': amount,
        'gas': gas_estimate,
        'gasPrice': gas_price,
        'nonce': web3.eth.get_transaction_count(account.address),
        'chainId': 56  # Chain ID của BSC Mainnet
    }

    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    try:
        receipt = wait_for_transaction_receipt(web3, txn_hash)
    except TimeoutError as e:
        print(str(e))

    return txn_hash
'''

def bsc_sendToken(seed, address, tokenAddress):
    # Kết nối tới nút BSC
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(seed)

    token_contract_address = Web3.to_checksum_address(tokenAddress)

    erc20_abi = [
        {
            "constant": False,
            "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        }
    ]

    token_contract = web3.eth.contract(address=token_contract_address, abi=erc20_abi)
    balance = token_contract.functions.balanceOf(account.address).call()
    if balance == 0:
        raise ValueError("Không có đủ số dư để thực hiện giao dịch")

    amount = balance

    # Ước lượng gas
    gas_estimate = token_contract.functions.transfer(address, amount).estimate_gas({
        'from': account.address
    })


    transaction = token_contract.functions.transfer(address, amount).build_transaction({
        'gas': gas_estimate,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(account.address),
        'chainId': 56
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    try:
        receipt = wait_for_transaction_receipt(web3, txn_hash)
    except TimeoutError as e:
        print(str(e))

    return txn_hash
def bsc_sendBnb(seed, recipient_address):
    # Kết nối tới nút BSC
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(Web3.HTTPProvider(bsc))

    if not web3.is_connected():
        raise ConnectionError("Không thể kết nối tới BSC")

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(seed)

    balance = web3.eth.get_balance(account.address)
    gas_price = web3.eth.gas_price

    # Ước lượng gas
    transaction = {
        'to': Web3.to_checksum_address(recipient_address),
        'value': balance,  # Giá trị sẽ được điều chỉnh sau
        'gasPrice': gas_price,
        'nonce': web3.eth.get_transaction_count(account.address),
        'chainId': 56
    }
    gas_estimate = web3.eth.estimate_gas(transaction)
    gas_cost = gas_estimate * gas_price


    # Số dư khả dụng để gửi (trừ phí gas)
    amount = balance - gas_cost

    if amount <= 0:
        raise ValueError("Số dư không đủ để thanh toán phí gas.")

    transaction['value'] = amount
    transaction['gas'] = gas_estimate

    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    try:
        receipt = wait_for_transaction_receipt(web3, txn_hash)
    except TimeoutError as e:
        print(str(e))

    return amount

def write_to_file(file_path, content):
    with open(file_path, 'a') as file: 
        file.write(content + "\n")

def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]