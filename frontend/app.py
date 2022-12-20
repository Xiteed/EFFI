import subprocess
from website import create_app

app = create_app()

if __name__ == '__main__':
    # Open subprocess to get ip address of device.
    p = subprocess.Popen(['hostname -I'], shell=True, stdout=subprocess.PIPE)
    p.wait()
    IP_address = p.stdout.readline()[:-2].decode('UTF-8')
    app.run(debug=True, host=IP_address, port=8080)
