import socket
from website import create_app

app = create_app()

h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

if __name__ == '__main__':
    app.run(debug=True, host=IP_addres, port=8080)
