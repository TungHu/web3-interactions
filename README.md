### web3-interactions
web3-interactions là một công cụ được xây dựng bằng Python để tương tác với các ứng dụng Web3. Repository này cung cấp các chức năng như gửi token, kiểm tra số dư, và thực hiện các giao dịch khác trên mạng blockchain Ethereum.

## Tính năng
- Gửi token (ETH hoặc token ERC-20) đến địa chỉ khác.
- Kiểm tra số dư ETH và token ERC-20 của ví.
- Tương tác với các smart contract.
- Tạo ví mới và quản lý ví từ seed phrase.
## Yêu cầu
- Python 3.7 trở lên
- Visual Studio Code (hoặc IDE Python khác)
## Cài đặt
1. Clone Repository
- Trước tiên, bạn cần clone repository về máy tính của mình:
```sh
git clone https://github.com/yourusername/web3-interactions.git
cd web3-interactions
```
2. Cài Đặt Môi Trường Ảo (Tùy chọn)
- Việc sử dụng môi trường ảo (virtual environment) giúp cô lập các thư viện của dự án với các dự án khác:
```sh
python -m venv env
source env/bin/activate   # Trên Windows
env\Scripts\activate      # Trên macOS/Linux
```
3. Cài Đặt Thư Viện Cần Thiết
- Repository này đi kèm với một file requirements.txt chứa danh sách các thư viện cần thiết. Bạn có thể cài đặt chúng bằng pip:
```sh
pip install -r requirements.txt
```
