import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 4000

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server_socket = None
        self.max_message_size = 1024


        self.clients = []
        self.clients_lock = threading.Lock()

        self.is_running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(50)

        self.is_running = True
        print(f"SERVER ONLINE {self.host}:{self.port}")

        threading.Thread(target=self.accept_client, daemon=True).start()

    def accept_client(self):
        while self.is_running:
            try:
                client_socket, addr = self.server_socket.accept()

                with self.clients_lock:
                    self.clients.append(client_socket)

                print(f"Client connected: {addr}")

            except:
                pass

    def disconnect_client(self, client_socket=None):

        if client_socket is None:
            with self.clients_lock:
                clients_copy = list(self.clients)
            for cs in clients_copy:
                self.disconnect_client(cs)
            return

        with self.clients_lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)

        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            client_socket.close()
        except Exception:
            pass

    def stop(self):
        self.is_running = False
        self.disconnect_client()

        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None

        print("SERVER OFFLINE")

    def send(self, text):

        data = text.encode()

        to_remove = []
        with self.clients_lock:
            for client_socket in self.clients:
                try:
                    client_socket.send(data)
                except Exception:
                    to_remove.append(client_socket)


        for cs in to_remove:
            self.disconnect_client(cs)





server = Server(HOST, PORT)
server.start()

prepared_message = "SERVER: ПОВІТРЯНА ТРИВОГА\n"

try:
    while True:
        server.send(prepared_message)
        print("ПОВІДОМЛЕННЯ НАДІСЛАНО")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nЗАВЕРШЕНО")
finally:
    server.stop()