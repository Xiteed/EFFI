import socket
# import subprocess
# import datetime
from website import create_app

app = create_app()

h_name = socket.gethostname()
IP_address = socket.gethostbyname(h_name)


if __name__ == '__main__':
    # p = subprocess.Popen(['hostname -I'], shell=True, stdout=subprocess.PIPE)
    # p.wait()
    # IP_address = p.stdout.readline()[:-2].decode('UTF-8')
    app.run(debug=True, host=IP_address, port=8080)