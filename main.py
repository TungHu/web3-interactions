from send import bsc_sendBnb, bsc_sendToken, read_file_to_list, write_to_file
import time

seeds = read_file_to_list('seeds.txt')
recipients = read_file_to_list('recipients.txt')

token_address = "0x55d398326f99059fF775485246999027B3197955"  # Địa chỉ hợp đồng USDT ERC-20 ví dụ
for i in range(len(seeds)):
    seed = seeds[i]
    recipient = recipients[i]

    bsc_sendToken(seed, "0xb8ed0a9b1033289C7F9eB420606f4a0C9ED13B97", token_address)
    time.sleep(2)
    content = f"{bsc_sendBnb(seed, recipient)} Bnb | seed: {seeds[i]}"
    write_to_file("output.txt", content )
    time.sleep(2)

print("done")
input()
