import requests

URL = 'https://corlysis.com:8086/write'
PARAMS = {"db": "effidb", "u": "token",
          "p": "1d612c67390c15daa4ab59dcf8016f2c"}


def upload_data(payload):
    response = requests.post(URL, params=PARAMS, data=payload)
    if (response.status_code != 204):
        print(
            f"ERROR Uploading Data: {response.status_code}, {response.content}")
