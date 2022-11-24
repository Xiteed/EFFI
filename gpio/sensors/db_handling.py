import requests

URL = 'https://corlysis.com:8086/write'
PARAMS = {"db": "test_db", "u": "token",
          "p": "1d612c67390c15daa4ab59dcf8016f2c"}


def upload_data(payload):
    r = requests.post(URL, params=PARAMS, data=payload)
    print(f'Response code: {r.status_code}')


if __name__ == '__main__':
    payload = "temp_test temperature=26.64,humidity=15.53\n"
    upload_data(payload)
