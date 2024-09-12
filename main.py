import requests
import user_agent
from config import UNISAT_API_KEY



with open('address.txt', 'r') as f:
    addresses = [row.strip() for row in f]




def make_request(method: str = 'POST', url: str = None, headers: dict = None, params: dict = None, data: str = None, json: dict = None):
    s = requests.Session()
    response = s.request(method, url, headers=headers, params=params, data=data, json=json)
    return response.json()


headers = {
    'accept': 'application/json, text/plain, */*',
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
    'Content-Type': 'application/json',
    "origin": "https://unisat.io",
    "referer": "https://unisat.io/",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": user_agent.generate_user_agent(),
    'Authorization': f'Bearer {UNISAT_API_KEY}',
}


i = 0
sum = 0
while addresses:
    i += 1
    address = addresses.pop(0)
    url1 = f"https://open-api.unisat.io/v1/indexer/address/{address}/balance"
    response1 = make_request(method="GET", url=url1, headers=headers)
    url2 = f"https://open-api.unisat.io/v1/indexer/address/{address}/runes/balance-list"
    response2 = make_request(method="GET", url=url2, headers=headers)
    account_info = response1['data']

    try:
        s = response2['data']
        s = s['detail']
        r = int(s[0].get('amount')) * 410
        runes = 0
        for ss in s:
            if ss.get('runeid') == '860819:1238':
                runes = runes + (int(ss.get('amount')) /  9500000)
            else:
                runes = runes + (int(ss.get('amount')))

    except Exception as e:
        r = 0
    print(f"Wallet: {i} [{int(account_info.get('satoshi')) - r} satoshi]  [ {account_info.get('inscriptionUtxoCount') + runes} points]")
    sum = account_info.get('utxoCount') + sum
print(f'Total: {sum} points')



