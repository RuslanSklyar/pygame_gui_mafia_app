import socket
import json


class Client:
    def __init__(self, api):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.client_socket.connect(("localhost", 9999))
        self.api = api

    def send(self):
        # считывае информацию игрока
        message = json.dumps(self.api).encode()
        # отправляем данные на сервер
        self.client_socket.sendall(message)

    def get(self):
        # получаем ответ от сервера
        data = self.client_socket.recv(4096)
        data = data.decode()
        data = json.loads(data)
        return data
