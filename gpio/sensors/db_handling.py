import requests

URL = 'https://corlysis.com:8086/write'
PARAMS = {"db": "effidb", "u": "token",
          "p": "24378526400017a008459a68bf933251"}


def upload_data(payload):
    response = requests.post(URL, params=PARAMS, data=payload)
    if (response.status_code != 204):
        print(
            f"ERROR Uploading Data: {response.status_code}, {response.content}")


if __name__ == "__main__":
    upload_data('air_quality moisture=412,tank_volume=3.15\n')
