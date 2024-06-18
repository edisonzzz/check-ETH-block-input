import requests
import codecs

# 获取最新的区块号
def get_latest_block_number():
    url = "https://mainnet.infura.io/v3/xxx"  # 替换成你的 Infura 项目 ID
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }

    response = requests.post(url, headers=headers, json=data)
    print("Fetching latest block number...")
    if response.status_code == 200:
        result = response.json()
        if "result" in result and result["result"]:
            return int(result["result"], 16)
    return None

# 获取指定区块的所有交易的 input 信息
def get_block_transactions_input(block_number):
    url = "https://mainnet.infura.io/v3/xxx"  # 替换成你的 Infura 项目 ID
    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],  # 设置为 True 以获取交易信息
        "id": 1
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Fetching block {block_number}...")
    if response.status_code == 200:
        result = response.json()
        if "result" in result and result["result"] and "transactions" in result["result"]:
            transactions = result["result"]["transactions"]
            block_transactions_input = []

            for tx in transactions:
                tx_hash = tx["hash"]
                tx_input = get_transaction_input(tx_hash)
                block_transactions_input.append({
                    "hash": tx_hash,
                    "input": tx_input
                })

            return block_transactions_input
    return None

# 获取指定交易的 input 信息
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
        print(f"Failed to decode input data: {e}")
        return input_data_hex

# 将交易 input 信息写入到 txt 文件中
def write_transactions_input_to_txt(block_number, transactions_input):
    if transactions_input:
        with open(f"latest_block_transactions_input.txt", "w") as file:
            for tx in transactions_input:
                decoded_input = decode_input_data(tx['input'])
                file.write(f"Block {block_number}, Transaction {tx['hash']} Input Data:\n{decoded_input}\n\n")
        print(f"最新区块 {block_number} 中所有交易的 input 信息已写入到 latest_block_transactions_input.txt 文件中。")
    else:
        print(f"获取最新区块 {block_number} 中的交易信息失败。")

# 主函数
def main():
    latest_block_number = get_latest_block_number()
    if latest_block_number:
        block_transactions_input = get_block_transactions_input(latest_block_number)
        write_transactions_input_to_txt(latest_block_number, block_transactions_input)
    else:
        print("获取最新的区块高度失败。")

if __name__ == "__main__":
    main()
