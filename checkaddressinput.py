import requests
import codecs

# 获取指定地址的所有交易记录
def get_address_transactions(address):
    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "apikey": "xxx"  # 替换为你的 Etherscan API Key
    }

    response = requests.get(url, params=params)
    print(f"Fetching transactions for address {address}...")
    if response.status_code == 200:
        result = response.json()
        if "result" in result:
            return result["result"]
    return None

# 获取交易的 input 信息
def get_transaction_input(tx_hash):
    url = "https://mainnet.infura.io/v3/xxx"  # 替换成你的 Infura 项目 ID
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionByHash",
        "params": [tx_hash],
        "id": 1
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Fetching transaction {tx_hash}...")
    if response.status_code == 200:
        result = response.json()
        if "result" in result and result["result"]:
            tx_input = result["result"]["input"]
            return tx_input
    return None

# 尝试将十六进制字符串解码为 UTF-8 文本
def decode_input_data(input_data_hex):
    try:
        input_data_bytes = codecs.decode(input_data_hex[2:], "hex")
        input_data_text = input_data_bytes.decode("utf-8")
        return input_data_text
    except Exception as e:
        # print(f"Failed to decode input data: {e}")
        return None

# 将交易的输入数据写入到 txt 文件中
def write_input_to_txt(file, input_data):
    if input_data:
        decoded_input = decode_input_data(input_data)
        if decoded_input is not None:
            file.write(f"{decoded_input}\n\n")

# 将交易的输入数据写入到 txt 文件中
def write_transactions_input_to_txt(address, transactions):
    if transactions:
        with open(f"address_{address}_transactions_input.txt", "w") as file:
            for tx in transactions:
                tx_input = get_transaction_input(tx["hash"])
                write_input_to_txt(file, tx_input)
        print(f"地址 {address} 的所有交易输入数据已写入到 address_{address}_transactions_input.txt 文件中。")
    else:
        print(f"Failed to fetch transactions for address {address}.")

# 查看指定地址的所有交易记录
def view_address_transactions_input(address):
    transactions = get_address_transactions(address)
    write_transactions_input_to_txt(address, transactions)

if __name__ == "__main__":
    # 指定要查询的地址
    address = "0xC226bBCa5Cbb0b45F8106772A6184DEAf5C1930A"  # 替换为你感兴趣的地址
    view_address_transactions_input(address)
