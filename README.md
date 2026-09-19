# Web3-interactions

Công cụ Python tương tác với các mạng EVM: gửi native coin, gửi token ERC-20, và swap token qua router kiểu Uniswap V2. Toàn bộ chức năng chạy ở dạng thư viện (`send.py`) hoặc script gửi hàng loạt (`main.py`).

## Tính năng

- Gửi token ERC-20 (toàn bộ số dư) tới một địa chỉ khác.
- Gửi native coin (BNB / ETH / MATIC) với số dư còn lại sau khi trừ phí gas.
- Swap token qua router Uniswap V2 style (tự động `approve` khi cần).
- Sinh địa chỉ EVM từ seed phrase (BIP-44, mặc định `m/44'/60'/0'/0/0`).
- Chạy hàng loạt: đọc danh sách seed phrase từ file, gửi lần lượt, ghi log.
- Hỗ trợ BSC Testnet để thử trước khi chạy mainnet.

## Các chain hỗ trợ

| Chain | chain_id | RPC mặc định | Router |
|---|---|---|---|
| Ethereum | 1 | `mainnet.infura.io/v3/<PROJECT_ID>` | Uniswap V2 Router |
| BSC | 56 | `https://bsc-dataseed.binance.org/` | PancakeSwap V2 Router |
| Polygon | 137 | `https://polygon-rpc.com/` | QuickSwap Router |
| Arbitrum One | 42161 | `https://arb1.arbitrum.io/rpc` | SushiSwap Router |
| Base | 8453 | `https://mainnet.base.org` | (giá trị ví dụ trong code) |
| BSC Testnet | 97 | `data-seed-prebsc-1-s1.binance.org:8545` | - |

Mỗi chain trong biến `CHAINS` (trong `send.py`) gồm: `name`, `rpc_url`, `chain_id`, `router_address`, `wrapped_native_address`.

> **Lưu ý:**
> - `send_funds()` và `swap_token()` nhận `chain_info` nên chạy được trên mọi chain có trong `CHAINS`.
> - Các hàm `bsc_*` và `arbitrum_*` hardcode RPC và chainId trong code, chỉ dùng cho BSC / Arbitrum.
> - `CHAINS['base']` hiện dùng `router_address` và `wrapped_native_address` là giá trị ví dụ - hãy thay bằng địa chỉ chính thức trước khi dùng thật.
> - `CHAINS['ethereum']` cần Infura Project ID.

## Yêu cầu

- Python 3.12 (đã kiểm thử với 3.12.6)
- Các thư viện trong `requirements.txt` (chính: `web3==7.2.0`, `eth-account==0.13.3`, `pycryptodome`, `pydantic`)

## Cài đặt

1. Clone repository:

```sh
git clone https://github.com/TungHu/web3-interactions.git
cd web3-interactions
```

2. Tạo môi trường ảo (khuyến nghị):

```sh
python -m venv env
```

Kích hoạt môi trường ảo:

```sh
# Windows (PowerShell / CMD)
env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

3. Cài thư viện:

```sh
pip install -r requirements.txt
```

4. (Tuỳ chọn) Mở thư mục bằng Visual Studio Code, hoặc mở solution `main.sln` / project `main.pyproj` bằng Visual Studio có cài Python workload.

## Cấu trúc dự án

```text
web3-interactions/
|-- send.py            # Thư viện: CHAINS + các hàm gửi / swap
|-- main.py            # Script chạy hàng loạt (ví dụ workflow)
|-- requirements.txt
|-- recipients.txt     # Danh sách địa chỉ nhận (1 địa chỉ / dòng)
|-- seeds.txt          # Danh sách seed phrase (1 seed phrase / dòng)
|-- output.txt         # File log kết quả
|-- main.sln / main.pyproj
`-- README.md
```

`seeds.txt`, `output.txt` và các file chứa seed khác đã có trong `.gitignore` - **không** đưa chúng lên Git.

## Hướng dẫn sử dụng

### 1. Gửi native coin

```python
from send import CHAINS, send_funds

seed = "word1 word2 ... word12"
txn_hash = send_funds(seed, "0xDiaChiNhan", CHAINS['arbitrum'])  # gửi hết ETH còn lại
print(txn_hash)
```

Giá trị gửi = toàn bộ số dư trừ phí gas ước lượng. Nếu số dư không đủ trả gas, hàm raise `ValueError("Số dư không đủ để thanh toán phí gas.")`.

### 2. Gửi token ERC-20

```python
from send import CHAINS, send_funds

USDT_arb = "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9"
txn_hash = send_funds(seed, "0xDiaChiNhan", CHAINS['arbitrum'], USDT_arb)
print(txn_hash)
```

Hàm gửi **toàn bộ** số dư token của ví. Nếu số dư bằng 0 sẽ raise `ValueError("Không có đủ số dư token để thực hiện giao dịch")`.

### 3. Swap token

```python
from send import CHAINS, swap_token

# Swap sang wrapped native (WBNB / WETH / ...)
txn_hash = swap_token(seed, CHAINS['bsc'], token_in="0xDiaChiTokenIn")

# Swap sang một token khác
txn_hash = swap_token(seed, CHAINS['bsc'], token_in="0xDiaChiTokenIn", token_out="0xDiaChiTokenOut")
```

- Không truyền `token_out` thì hàm swap sang wrapped native của chain (`wrapped_native_address`).
- Hàm tự kiểm tra `allowance` và gửi giao dịch `approve` cho router nếu còn thiếu.
- `amountOutMin` đang đặt bằng `0` (chấp nhận mọi mức giá), deadline 60 giây.
- Trả về hash dạng hex và **không** chờ receipt.
- Code chỉ swap sang wrapped native, **không** unwrap về coin gốc.

### 4. Dùng các hàm chuyên biệt cho BSC / Arbitrum

```python
from send import bsc_sendBnb, bsc_sendToken, arbitrum_sendEth, arbitrum_sendToken

USDT_bsc = "0x55d398326f99059ff775485246999027b3197955"
USDT_arb = "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9"

bsc_sendBnb(seed, "0xDiaChiNhan")                      # BSC mainnet (chainId 56)
bsc_sendToken(seed, "0xDiaChiNhan", USDT_bsc)          # BSC mainnet
arbitrum_sendEth(seed, "0xDiaChiNhan")                 # Arbitrum One (chainId 42161)
arbitrum_sendToken(seed, "0xDiaChiNhan", USDT_arb)     # Arbitrum One
```

Các hàm này **hardcode RPC** trong code, không đọc từ `CHAINS`. Hàm gửi native trả về số wei đã gửi, hàm gửi token trả về `txn_hash`.

### 5. Thử trên BSC Testnet

```python
from send import bsc_sendBnb_testnet, bsc_sendToken_testnet

usdt_testnet = "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd"
bsc_sendBnb_testnet(seed, "0xDiaChiNhan")                # chainId 97
bsc_sendToken_testnet(seed, "0xDiaChiNhan", usdt_testnet)
```

### 6. Sinh địa chỉ EVM từ seed phrase

```python
from main import generate_evm_address_from_seed

address = generate_evm_address_from_seed("word1 word2 ... word12")
print(address)

# Chỉ định derivation path khác (mặc định là m/44'/60'/0'/0/0)
address = generate_evm_address_from_seed(seed, "m/44'/60'/0'/0/1")
```

### 7. Chạy script hàng loạt

```sh
python main.py
```

Workflow hiện tại trong `main.py`:

1. Đọc danh sách seed từ file (biến `seed_file_path`).
2. Lấy `seeds[0]` làm ví gửi, sinh địa chỉ nhận từ `seeds[1]`.
3. Gửi USDC trên Base tới địa chỉ vừa sinh.
4. Xoá dòng seed vừa dùng khỏi file (`remove_first_line`) để lần chạy sau không dùng lại.
5. Lặp qua các seed còn lại và gửi USDT trên Arbitrum.

Sửa danh sách địa chỉ nhận trong `recipients.txt` (mỗi dòng một địa chỉ) và đường dẫn file seed trong `main.py` cho phù hợp với máy bạn.

## Bảng tham chiếu hàm

| Hàm | Tham số | Ghi chú |
|---|---|---|
| `send_funds(seed, recipient_address, chain_info, token_address=None)` | `chain_info` lấy từ `CHAINS` | Không có `token_address` thì gửi native; có thì gửi hết token. Trả về hex hash hoặc số token đã gửi |
| `bsc_sendBnb(seed, recipient_address)` | | Trả về số wei đã gửi |
| `bsc_sendToken(seed, address, tokenAddress)` | | Trả về `txn_hash` |
| `bsc_sendBnb_testnet(seed, recipient_address)` | | Chain ID 97 |
| `bsc_sendToken_testnet(seed, address, tokenAddress)` | | Chain ID 97 |
| `arbitrum_sendEth(seed, recipient_address)` | | Trả về số wei đã gửi |
| `arbitrum_sendToken(seed, address, tokenAddress)` | | Trả về `txn_hash` |
| `swap_token(seed, chain_info, token_in, token_out=None)` | | Swap 100% số dư `token_in` |
| `wait_for_transaction_receipt(web3, txn_hash, timeout=120)` | | Poll 1 giây/lần; quá 120 giây chỉ in cảnh báo rồi thoát, không raise |
| `read_file_to_list(file_path)` | | Đọc file thành list, mỗi dòng một phần tử |
| `write_to_file(file_path, content)` | | Ghi nối thêm một dòng vào file |

## Bảo mật - đọc trước khi dùng

- **Không bao giờ commit seed phrase.** Các file seed (`seeds.txt`, `seed_bsx.txt`) và `output.txt` đã được ignore; kiểm tra lại bằng `git status` trước mỗi lần push.
- Seed phrase đã nằm trong git history thì coi như đã lộ vĩnh viễn - phải chuyển tài sản sang ví mới.
- `CHAINS['ethereum']['rpc_url']` cần Infura Project ID: nên đặt qua biến môi trường thay vì ghi thẳng vào code, vì API key trong file đã commit là key công khai.
- Hầu hết các hàm gửi **toàn bộ số dư** - hãy thử trên testnet hoặc với số tiền nhỏ trước.
- `swap_token` đặt `amountOutMin = 0`, không bảo vệ trượt giá. Chỉ dùng với pool có thanh khoản tốt.

## Lỗi thường gặp

| Lỗi | Nguyên nhân / cách xử lý |
|---|---|
| `Không thể kết nối tới <chain>` | RPC sai hoặc mất mạng; thay `rpc_url` trong `CHAINS` |
| `Không có đủ số dư để thực hiện giao dịch` | Số dư token bằng 0 (`bsc_sendToken`, `arbitrum_sendToken`) |
| `Không có đủ số dư token để thực hiện giao dịch` | Số dư token bằng 0 khi gọi `send_funds` |
| `Số dư không đủ để thanh toán phí gas.` | Ví không đủ native coin để trả phí gas |
| `Số dư không đủ để swap` | Số dư `token_in` bằng 0 |
| Lỗi validate địa chỉ / `Web3ValidationError` | Địa chỉ phải đúng chuẩn checksum EIP-55; dùng `Web3.to_checksum_address()` |
| `FileNotFoundError` khi chạy `main.py` | Thiếu file seed / `recipients.txt`, hoặc sai đường dẫn trong biến `seed_file_path` |
| Giao dịch chờ quá lâu không có kết quả | Hàm chờ tối đa 120 giây, sau đó chỉ in cảnh báo rồi thoát; kiểm tra hash trên block explorer |
| RPC trả `429 Too Many Requests` | RPC công cộng bị giới hạn; dùng nhà cung cấp RPC riêng (Alchemy / Infura / Ankr) |

## Miễn trừ trách nhiệm

Dự án phục vụ mục đích học tập và nghiên cứu. Người dùng tự chịu trách nhiệm với mọi giao dịch, thiệt hại tài chính và việc tuân thủ pháp luật tại nơi mình sinh sống.
