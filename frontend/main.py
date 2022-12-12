import socket
# import subprocess
from website import create_app

app = create_app()

h_name = socket.gethostname()
IP_address = socket.gethostbyname(h_name)


if __name__ == '__main__':
    # p = subprocess.Popen(['hostname -I'], shell=True)
    # p.wait()
    # out, err = p.communicate()
    # IP_address = out
    app.run(debug=True, host=IP_address, port=8080)
