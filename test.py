import sys
import argparse
import requests

"""

python test.py 1 token1 <host> <port(if not 8000)>
"""

def fetch_creds(uId: str, token: str, host: str, port: int):
    url = f"http://{host}:{port}/fetch_creds"
    params = {'uId': uId, 'acc_token': token}
    resp = requests.get(url, params=params)

    if resp.status_code == 200:
        creds = resp.json()
        print(f"Name:     {creds['name']}")
        print(f"Account:  {creds['account']}")
        print(f"Password: {creds['password']}")
    else:
        print(f"Error {resp.status_code}: {resp.json().get('error')}")

def main():
    p = argparse.ArgumentParser(description="example script for credential fetcher")
    p.add_argument('uId')
    p.add_argument('acc_token')
    p.add_argument('--host',     default='localhost')
    p.add_argument('--port',     type=int, default=8000)
    args = p.parse_args()

    fetch_creds(args.uId, args.acc_token, args.host, args.port)

if __name__ == '__main__':
    main()