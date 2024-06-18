import requests
from bs4 import BeautifulSoup

def get_top_holders(limit=1000):
    url = "https://etherscan.io/accounts"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    holders = []
    page = 1
    
    while len(holders) < limit:
        response = requests.get(url, headers=headers, params={"p": page})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find("table", {"class": "table"})
        if not table:
            break
        
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                print(f"Skipping row with insufficient columns: {cols}")
                continue  # Skip rows that don't have enough columns

            address = cols[1].text.strip()
            balance_text = cols[2].text.strip().split()[0].replace(',', '')
            try:
                balance = float(balance_text)
                holders.append((address, balance))
            except ValueError:
                print(f"Skipping row with invalid balance: {balance_text}")
                continue  # Skip rows with invalid balance
            
            if len(holders) >= limit:
                break
        
        page += 1
    
    return holders

def main():
    top_holders = get_top_holders(limit=1000)
    
    with open('top_holders.txt', 'w') as file:
        for index, holder in enumerate(top_holders, start=1):
            line = f"{index}. Address: {holder[0]}, Balance: {holder[1]:,.4f} ETH\n"
            file.write(line)
    
    print("Top 1000 holders have been written to top_holders.txt")

if __name__ == '__main__':
    main()
