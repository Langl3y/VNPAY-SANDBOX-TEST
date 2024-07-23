import hashlib
import hmac
import requests
from datetime import datetime
import urllib.parse

import os
from dotenv import load_dotenv

load_dotenv()

vnp_TmnCode = os.getenv('TMN_CODE')
vnp_HashSecret = os.getenv('HASH_SECRET')
vnp_Url = os.getenv('SANDBOX_URL')


def generate_secure_hash(payload, secret_key):
    sorted_payload = sorted(payload.items())
    data_string = '&'.join(f"{key}={urllib.parse.quote_plus(str(value))}" for key, value in sorted_payload)
    secure_hash = hmac.new(secret_key.encode(), data_string.encode(), hashlib.sha512).hexdigest()
    return secure_hash


def get_payment_url():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    payload = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': vnp_TmnCode,
        'vnp_Amount': str(int(10000 * 100)),
        'vnp_CreateDate': timestamp,
        'vnp_CurrCode': 'VND',
        'vnp_IpAddr': '127.0.0.1',
        'vnp_Locale': 'vn',
        'vnp_OrderInfo': 'Test',
        'vnp_OrderType': '130005',
        'vnp_ReturnUrl': 'https://domain.vn/VnPayReturn',
        'vnp_TxnRef': '121535262'
    }

    payload['vnp_SecureHash'] = generate_secure_hash(payload, vnp_HashSecret)

    final_url = f"{vnp_Url}?{urllib.parse.urlencode(payload)}"

    response = requests.get(final_url)
    print(response.url)


if __name__ == "__main__":
    get_payment_url()
