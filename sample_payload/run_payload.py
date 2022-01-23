import argparse
import json

import requests
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Target host of the endpoint. (i.e. "0.0.0.0:1337")', default='0.0.0.0:1337')
    parser.add_argument('payload', help='Payload JSON path. In JSON List format.')

    args = parser.parse_args()
    return args


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def main():
    args = get_args()

    payload_list = load_json(args.payload)
    total_payload = len(payload_list)

    for idx, payload in enumerate(payload_list, start=1):
        print(' ')
        endpoint = f'http://{args.host}/predict_income'
        
        print(f'[{idx}/{total_payload}] Sending Payload: ')
        print(payload)
        print(' ')
        req = requests.post(endpoint, json=payload)
        result = req.json()

        print(f'[{idx}/{total_payload}] Received response: ')
        print(result)
        print(' ')


if __name__ == '__main__':
    main()
