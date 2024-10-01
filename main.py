from xml.etree.ElementTree import tostring
from send import CHAINS, bsc_sendBnb, bsc_sendToken, read_file_to_list, send_funds, swap_token, write_to_file, bsc_sendBnb_testnet,bsc_sendToken_testnet
import time
from web3 import Web3

seeds = read_file_to_list('seeds.txt')
recipients = read_file_to_list('recipients.txt')
BINANCEH = '0x8c41f0ce2dba04f6b014bae7e183b2ad9aea0c47'
GATEH = '0x6FcD1737352905fBFEC0F3AD7375DFA0d7ECC98f'
USDT_bsc = "0x55d398326f99059fF775485246999027B3197955"  # Địa chỉ hợp đồng USDT ERC-20
usdt_testnet = "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd"
Tung_gom = "0xd75946295A3DfFB837ea276902032859576c53Be"
SNIFT_bsc = '0x5c4625aC040486cE7A9054924B8cd3E4Ba8480a6'
for i in range(len(seeds)):
    seed = seeds[i]
    content = str(i) + " "

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
    
    try:
        txn_hash = send_funds(seed, Tung_gom, CHAINS['arbitrum'])
    except Exception as e: print(e)

    try:
        time.sleep(2)
        txn_hash = send_funds(seed, Tung_gom, CHAINS['bsc'], SNIFT_bsc)
    except Exception as e: print(e)

    
    try:
        time.sleep(2)
        txn_hash = send_funds(seed, recipients[i], CHAINS['bsc'])
    except Exception as e: print(e)
  
    content += txn_hash
    
    print(f"Giao dịch gửi token: {txn_hash}")

    write_to_file("output.txt", content )
    time.sleep(2)


'''for i in range(len(seeds)):
    seed = seeds[i]
    recipient = recipients[i]

    bsc_sendToken_testnet(seed, "0xb8ed0a9b1033289C7F9eB420606f4a0C9ED13B97", usdt_testnet)
    time.sleep(2)
    content = f"{bsc_sendBnb_testnet(seed, recipient)} Bnb | seed: {seeds[i]}"
    write_to_file("output.txt", content )
    time.sleep(2)
    '''
print("done")
input()
