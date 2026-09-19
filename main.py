from xml.etree.ElementTree import tostring
from send import CHAINS, bsc_sendBnb, bsc_sendToken, read_file_to_list, send_funds, swap_token, write_to_file, bsc_sendBnb_testnet,bsc_sendToken_testnet
import time
from web3 import Web3
from eth_account import Account

seeds = read_file_to_list('seeds.txt')
recipients = read_file_to_list('recipients.txt')
BINANCEH = '0x8c41f0ce2dba04f6b014bae7e183b2ad9aea0c47'
GATEH = '0x6FcD1737352905fBFEC0F3AD7375DFA0d7ECC98f'
usdt_testnet = "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd"
Tung_gom = "0x2fe78c94d7a93d10E580921aFDc962f8e6172b12"
USDT_bsc = "0x55d398326f99059ff775485246999027b3197955"
sieu_gom = "0x8822b8AA510d8227FffF3Ce9063834abfd118D89"
GOF_arb = '0x85b7FA2a3Cfe5ED48B619EC967750462A1FD9557'
BTC_bsc = "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c"
ETH_bsc = '0x2170ed0880ac9a755fd29b2688956bd959f933f8'
USDT_arb = '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9'
USDC_base = '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913'



def write_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content + "\n")

def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def remove_first_line(file_path):
    """
    Xóa dòng đầu tiên trong file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        file.writelines(lines[1:])  # Ghi lại các dòng từ dòng thứ 2 trở đi.
def generate_evm_address_from_seed(seed_phrase, derivation_path="m/44'/60'/0'/0/0"):
    """
    Từ seed phrase sinh ra địa chỉ EVM.
    
    Args:
        seed_phrase (str): Seed phrase (mnemonic).
        derivation_path (str): Đường dẫn dẫn xuất BIP-44 (mặc định là cho EVM).

    Returns:
        str: Địa chỉ EVM được sinh ra.
    """
    # Bật tính năng HD Wallet chưa được kiểm duyệt
    Account.enable_unaudited_hdwallet_features()
    
    # Tạo tài khoản từ seed phrase với đường dẫn dẫn xuất
    account = Account.from_mnemonic(seed_phrase, account_path=derivation_path)
    
    # Trả về địa chỉ EVM
    return account.address



# Đường dẫn tệp chứa các seed
seed_file_path = r'C:\Users\ADMIN\source\repos\code\web3-interactions\seed_bsx.txt'

# Đọc danh sách seed ban đầu
seeds = read_file_to_list(seed_file_path)

# Thực hiện gửi token

sender_seed = seeds[0]
recipient_evm = generate_evm_address_from_seed(seeds[1])  # Seed tiếp theo là người nhận
txn_hash = ""

try:
    # Gọi hàm send_funds
    txn_hash = send_funds(sender_seed, recipient_evm, CHAINS['base'], USDC_base)
    print(f"|Giao dịch gửi token: {txn_hash}")

    # Xóa dòng đầu tiên trong tệp
    remove_first_line(seed_file_path)
    seeds = read_file_to_list(seed_file_path)  # Cập nhật danh sách seeds
    time.sleep(2)  # Tạm dừng 2 giây để tránh spam
except Exception as e:
    print(e)

print("done_")

for i in range(len(seeds)):
    seed = seeds[i]
    content = str(i) + " "
    txn_hash = ""
    '''try: #Web3.to_checksum_address()
        bsc_sendToken(seed, MAO_gom, MAO_address)
        print(f"{i} | {seed.split(" ")[0]} | MAO")
    except Exception as e:
        print(f"{i} | {seed.split(" ")[0]} | Error: {e} ")
    
    time.sleep(2)
    try:
        bsc_sendToken(seed, LOVE_gom, USDT_bsc)
        print(f"{i} | {seed.split(" ")[0]} | USDT")

    except Exception as e:
         print(f"{i} | {seed.split(" ")[0]} | Error: {e} ")
    
    time.sleep(2)
    try:
         content = f"{bsc_sendBnb(seed, recipients[i])} Bnb | seed: {seeds[i]}"
    except :
        pass
    '''
    #txn_hash = swap_token(seed,  CHAINS['bsc'],SNIFT_bsc)
    #print(f"Giao dịch swap đã gửi trên BSC: {txn_hash}")

    # Gửi eth
    
    '''try:
        txn_hash = send_funds(seed, Tung_gom, CHAINS['arbitrum'])
    except Exception as e: print(e)
    '''
    
    try:
        txn_hash = send_funds(seed, Web3.to_checksum_address(BINANCEH), CHAINS['arbitrum'], USDT_arb)
        #txn_hash = send_funds(seed, Web3.to_checksum_address(BINANCEH), CHAINS['bsc'])
        time.sleep(2)
    except Exception as e: print(e)

    print(f"Giao dịch gửi token: {txn_hash}")


    #time.sleep(2)



print("done")
input()
