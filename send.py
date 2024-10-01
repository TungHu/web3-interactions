
from web3 import Web3
from eth_account import Account
import time

UNISWAP_V2_ROUTER_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "amountIn", "type": "uint256"},
            {"name": "amountOutMin", "type": "uint256"},
            {"name": "path", "type": "address[]"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [{"name": "amounts", "type": "uint256[]"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

'''CHAINS = {
    'ethereum': {
        'name': 'Ethereum',
        'rpc_url': 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID',
        'chain_id': 1,
        'router_address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'  # Uniswap V2 Router
    },
    'bsc': {
        'name': 'Binance Smart Chain',
        'rpc_url': 'https://bsc-dataseed.binance.org/',
        'chain_id': 56,
        'router_address': '0x10ED43C718714eb63d5aA57B78B54704E256024E'  # PancakeSwap V2 Router
    },
    'polygon': {
        'name': 'Polygon',
        'rpc_url': 'https://polygon-rpc.com/',
        'chain_id': 137,
        'router_address': '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'  # QuickSwap Router
    },
    'arbitrum': {
        'name': 'Arbitrum',
        'rpc_url': 'https://arb1.arbitrum.io/rpc',
        'chain_id': 42161,
        'router_address': '0x1b02da8cb0d097eb8d57a175b88c7d8b47997506'  # SushiSwap Router
    }
}
    '''
CHAINS = {
    'ethereum': {
        'name': 'Ethereum',
        'rpc_url': 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID',
        'chain_id': 1,
        'router_address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',  # Uniswap V2 Router
        'wrapped_native_address': '0xC02aaa39b223FE8D0A0e5C4F27eAD9083C756Cc2'  # WETH (Wrapped Ether)
    },
    'bsc': {
        'name': 'Binance Smart Chain',
        'rpc_url': 'https://bsc-dataseed.binance.org/',
        'chain_id': 56,
        'router_address': '0x10ED43C718714eb63d5aA57B78B54704E256024E',  # PancakeSwap V2 Router
        'wrapped_native_address': '0xBB4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'  # WBNB (Wrapped BNB)
    },
    'polygon': {
        'name': 'Polygon',
        'rpc_url': 'https://polygon-rpc.com/',
        'chain_id': 137,
        'router_address': '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff',  # QuickSwap Router
        'wrapped_native_address': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619'  # WMATIC (Wrapped MATIC)
    },
    'arbitrum': {
        'name': 'Arbitrum',
        'rpc_url': 'https://arb1.arbitrum.io/rpc',
        'chain_id': 42161,
        'router_address': '0x1b02da8cb0d097eb8d57a175b88c7d8b47997506',  # SushiSwap Router
        'wrapped_native_address': '0x82af49447d8a07e3bd95bd0d56f35241523fbab1'  # WETH on Arbitrum
    }
}
  
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
    #amount = balance % 505000000000000000000
    #amount = 5171720543860793533
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

def bsc_sendToken_testnet(seed, address, tokenAddress):
    # Kết nối tới nút BNB Testnet
    bsc_testnet = "https://data-seed-prebsc-1-s1.binance.org:8545/"
    web3 = Web3(Web3.HTTPProvider(bsc_testnet))

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
        'chainId': 97  # Testnet chain ID
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    try:
        receipt = wait_for_transaction_receipt(web3, txn_hash)
    except TimeoutError as e:
        print(str(e))

    return txn_hash

def bsc_sendBnb_testnet(seed, recipient_address):
    # Kết nối tới nút BNB Testnet
    bsc_testnet = "https://data-seed-prebsc-1-s1.binance.org:8545/"
    web3 = Web3(Web3.HTTPProvider(bsc_testnet))

    if not web3.is_connected():
        raise ConnectionError("Không thể kết nối tới BNB Testnet")

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
        'chainId': 97  # Testnet chain ID
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

def arbitrum_sendEth(seed, recipient_address):
    # Kết nối tới nút Arbitrum
    arbitrum = "https://arb1.arbitrum.io/rpc"
    web3 = Web3(Web3.HTTPProvider(arbitrum))

    if not web3.is_connected():
        raise ConnectionError("Không thể kết nối tới Arbitrum")

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
        'chainId': 42161  # Arbitrum chain ID
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

def arbitrum_sendToken(seed, address, tokenAddress):
    # Kết nối tới nút Arbitrum
    arbitrum = "https://arb1.arbitrum.io/rpc"
    web3 = Web3(Web3.HTTPProvider(arbitrum))

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
        'chainId': 42161  # Arbitrum chain ID
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    try:
        receipt = wait_for_transaction_receipt(web3, txn_hash)
    except TimeoutError as e:
        print(str(e))

    return txn_hash

def write_to_file(file_path, content):

    with open(file_path, 'a') as file: 
        file.write(content + "\n")

def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]
  
    
ERC20_ABI = [
       {
        "constant": True,
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def swap_token(seed, chain_info, token_in, token_out=None):
    
    web3 = Web3(Web3.HTTPProvider(chain_info['rpc_url']))
    if not web3.is_connected():
        raise ConnectionError(f"Không thể kết nối tới {chain_info['name']}")

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(seed)

    # Địa chỉ router tương ứng với chain
    uniswap_router_address = Web3.to_checksum_address(chain_info['router_address'])
    uniswap_router = web3.eth.contract(address=uniswap_router_address, abi=UNISWAP_V2_ROUTER_ABI)

    token_in_address = Web3.to_checksum_address(token_in)
    
    # Lấy ABI của ERC-20 token để lấy số dư
    token_contract = web3.eth.contract(address=token_in_address, abi=ERC20_ABI)
    amount_in_max = token_contract.functions.balanceOf(account.address).call()

    if amount_in_max == 0:
        raise ValueError("Số dư không đủ để swap")

    # Cấp quyền cho router sử dụng token
    allowance = token_contract.functions.allowance(account.address, uniswap_router_address).call()
    if allowance < amount_in_max:
        # Gọi hàm approve để cấp quyền
        approve_tx = token_contract.functions.approve(uniswap_router_address, amount_in_max).build_transaction({
            'from': account.address,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': chain_info['chain_id']
        })
        signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, account.key)
        web3.eth.send_raw_transaction(signed_approve_tx.raw_transaction)
        print("Đã cấp quyền cho router")

    # Kiểm tra nếu token_out là None thì swap sang native coin (BNB trên BSC)
    if token_out:
        token_out_address = Web3.to_checksum_address(token_out)
        path = [token_in_address, token_out_address]
        transaction = uniswap_router.functions.swapExactTokensForTokens(
            amount_in_max,
            0,  # Chấp nhận bất kỳ lượng token_out nào
            path,
            account.address,
            int(time.time()) + 60  # 60 giây hết hạn
        ).build_transaction({
            'from': account.address,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': chain_info['chain_id']
        })
    else:
        # Swap sang WBNB trên BSC, sau đó unwrap WBNB thành BNB nếu cần
        wrapped_native_address = Web3.to_checksum_address(chain_info['wrapped_native_address'])
        path = [token_in_address, wrapped_native_address]
        transaction = uniswap_router.functions.swapExactTokensForTokens(
            amount_in_max,
            0,  # Chấp nhận bất kỳ lượng WBNB nào
            path,
            account.address,
            int(time.time()) + 60  # 60 giây hết hạn
        ).build_transaction({
            'from': account.address,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': chain_info['chain_id']
        })

    # Ký và gửi giao dịch
    signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    return txn_hash.hex()

''' 
seed = "YOUR_MNEMONIC"
token_in = "0x6B175474E89094C44Da98b954EedeAC495271d0F"  # DAI
token_out = "0xC02aaA39b223FE8D0A0E5C4F27eAD9083C756Cc2"  # WETH

# Swap trên Arbitrum
txn_hash = swap_token(seed, token_in, token_out, CHAINS['arbitrum'])
print(f"Giao dịch swap đã gửi trên Arbitrum: {txn_hash}")

# Swap trên Binance Smart Chain
txn_hash = swap_token(seed, token_in, token_out, CHAINS['bsc'])
print(f"Giao dịch swap đã gửi trên BSC: {txn_hash}")
'''

def send_funds(seed, recipient_address, chain_info, token_address=None):

    web3 = Web3(Web3.HTTPProvider(chain_info['rpc_url']))

    if not web3.is_connected():
        raise ConnectionError(f"Không thể kết nối tới {chain_info['name']}")

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(seed)

    if token_address:
        # Gửi token ERC-20
        token_contract_address = Web3.to_checksum_address(token_address)
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
            raise ValueError("Không có đủ số dư token để thực hiện giao dịch")

        amount = balance
        gas_estimate = token_contract.functions.transfer(recipient_address, amount).estimate_gas({
            'from': account.address
        })

        transaction = token_contract.functions.transfer(recipient_address, amount).build_transaction({
            'gas': gas_estimate,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': chain_info['chain_id']
        })
    else:
        # Gửi native coin (ETH, BNB)
        balance = web3.eth.get_balance(account.address)
        #balance = 3310000000000000
        if (chain_info['name'] == 'Binance Smart Chain'):
            gas_price = web3.eth.gas_price
        else:
            
            latest_block = web3.eth.get_block('latest')
            base_fee_per_gas = latest_block['baseFeePerGas']
            gas_price = base_fee_per_gas + web3.to_wei(0, 'gwei')  # Thêm 2 gwei cho phí an toàn
        
        #gas_price = base_fee_per_gas + web3.to_wei(2, 'gwei')  # Thêm 2 gwei cho phí an toàn
        
        transaction = {
            'to': Web3.to_checksum_address(recipient_address),
            'value': balance,  # Giá trị sẽ được điều chỉnh sau
            'gasPrice': gas_price,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': chain_info['chain_id']
        }
        gas_estimate = web3.eth.estimate_gas(transaction)
        gas_cost = gas_estimate * gas_price

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

    return txn_hash.hex() if not token_address else amount

'''token_address = "0xTokenAddress"  # Địa chỉ token bạn muốn gửi

# Gửi token trên BSC Testnet
txn_hash = send_funds(seed, recipient, CHAINS['bsc'], token_address=token_address)
print(f"Giao dịch gửi token: {txn_hash}")

# Gửi token trên Arbitrum
txn_hash = send_funds(seed, recipient, CHAINS['arbitrum'], token_address=token_address)
print(f"Giao dịch gửi token: {txn_hash}")
'''
