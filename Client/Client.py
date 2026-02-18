import socket

HOST = '127.0.0.1'
PORT = 4000

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.max_message_size = 1024

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"CONNECTED TO {HOST}:{PORT}")

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    # def send(self, text):
    #     self.socket.send(text.encode())

    def receive(self):
        data = self.socket.recv(self.max_message_size)
        return data.decode()

client = Client(HOST, PORT)
client.connect()

try:
    while True:
        message = client.receive()
        if not message:
            print("SERVER DISCONNECTED")
            break
        print(message, end="")

except KeyboardInterrupt:
    print("\nCLIENT STOPPED")

finally:
    client.disconnect()