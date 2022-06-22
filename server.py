import socket
import json
import email_sender
from Rooms import Room


class User:
    def __init__(self, conn, s_addr):
        self.conn = conn
        self.addr = s_addr
        self.data_get_set = False
        self.errors = 0
        self.data = []


class Server:
    def __init__(self):
        # Создаем сокет
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server_socket.bind(("localhost", 9999))
        self.server_socket.setblocking(0)
        self.server_socket.listen(1)

        # база данных с пользователями
        self.base_data = {"~FLiN": ["flin4funads@gmail.com", "123454"], "Angel": ["123@gmail.com", "123454"],
                          "Asmansha123456": ["1234@gmail.com", "123454"]}

        # храним подключенные сокеты
        self.users = []  # Сокеты всех игроков
        self.active_room = []  # Объекты активных игровых комнат
        self.number_game = 0

        # регистрируем пользователей как игроков и судъей
        self.want_play = []
        self.want_judge = []

    def connect(self):
        # Подключения
        self.new_socket, self.addr = self.server_socket.accept()
        self.new_socket.setblocking(0)
        self.user = User(self.new_socket, self.addr)
        self.users.append(self.user)

    def get_data(self):
        for i in self.users:
            i.data = i.conn.recv(4096)
            if not i.data:
                i.errors += 1
            else:
                if not i.data_get_set:
                    i.errors = 0
                    i.data = i.data.decode()
                    i.data = self.prossesing_data(i, i.data)
                    i.data_get_set = True

    def prossesing_data(self, u_socket, user_data):
        user_data = json.loads(user_data)  # Разпаковка data

        # Проверка логина и пароля
        if user_data["window_see"]["sing_in"]:
            if len(user_data["sing_in"]["login"]) > 0 and len(user_data["sing_in"]["password"]) > 0:
                for k, v in self.base_data.items():
                    if k == user_data["sing_in"]["login"] or user_data["sing_in"]["login"] in v:
                        if user_data["sing_in"]["password"] in v:
                            user_data["sing_in"]["accept"] = True

        # регистрация нового пользователя
        if user_data["window_see"]["sing_up"]:
            if len(user_data["sing_up"]["login"]) > 0 and len(user_data["sing_up"]["e_mail"]) > 0 \
                    and len(user_data["sing_up"]["password_1"]) > 0 and len(user_data["sing_up"]["password_2"]) > 0:
                mail_index = ["@mail", "@gmail"]
                for k, v in self.base_data.items():
                    if user_data["sing_up"]["login"] != k:
                        if user_data["sing_up"]["e_mail"] not in v:
                            for mail in mail_index:
                                if mail in user_data["sing_up"]["e_mail"]:
                                    if user_data["sing_up"]["password_1"] == user_data["sing_up"]["password_2"]:
                                        if user_data["click"] == 1:
                                            user_data["sing_up"]["accept"] = True

        # отправка кода подтверждения пользователю на e-mail после регистрации
        if user_data["window_see"]["inpute_code"]:
            if user_data["sing_up"]["window_input"] is not True:
                user_data["sing_up"]["window_input"] = True
                email_sender.main(user_data["sing_up"]["code"], user_data["sing_up"]["e_mail"])
            else:
                if user_data["sing_up"]["inpute_code"] == user_data["sing_up"]["code"]:
                    self.base_data[user_data["sing_up"]["login"]] = [user_data["sing_up"]["e_mail"],
                                                                     user_data["sing_up"]["password_1"]]
                    user_data["sing_up"]["inpute_accept"] = True
                    user_data["window_see"]["sing_in"] = True

        # получаем из data статус "игрок"\"судья"
        if user_data["window_see"]["main_menu"]:
            if user_data["main_menu"]["status_player"]:
                if [u_socket, user_data["sing_in"]["login"]] not in self.want_play:
                    self.want_play.append([u_socket, user_data["sing_in"]["login"]])
            else:
                if [u_socket, user_data["sing_in"]["login"]] in self.want_play:
                    self.want_play.remove([u_socket, user_data["sing_in"]["login"]])

            if user_data["main_menu"]["status_judge"]:
                if [u_socket, user_data["sing_in"]["login"]] not in self.want_judge:
                    self.want_judge.append([u_socket, user_data["sing_in"]["login"]])
            else:
                if [u_socket, user_data["sing_in"]["login"]] in self.want_judge:
                    self.want_judge.remove([u_socket, user_data["sing_in"]["login"]])

            user_data["main_menu"]["len_status_player"] = len(self.want_play)
            user_data["main_menu"]["len_status_judge"] = len(self.want_judge)

        # Если пользователь зарегестрирован как игрок, впускаем его в игровую комнату.
        # Удаляем иго из списка желающих играть
        if user_data["window_see"]["main_menu"]:
            try:
                for i in self.active_room:
                    for p in i[0].all_usersInRoom:
                        if u_socket == p[0]:
                            user_data["window_see"]["lobby_room"] = True
                            if user_data["main_menu"]["status_player"]:
                                self.want_play.remove([u_socket, user_data["sing_in"]["login"]])
                            else:
                                self.want_judge.remove([u_socket, user_data["sing_in"]["login"]])
            except:
                pass

        user_data = json.dumps(user_data)
        return user_data  # Возвращаем data

    def user_errors_connection(self):
        for i in self.users:
            if i.errors == 10000000:
                i.conn.close()
                self.users.remove(i)

    # ---!!! Асинхронная ф-ция !!!---
    def create_room(self):
        if len(self.want_play) > 0 and len(self.want_judge) > 0:
            self.number_game += 1
            self.room = Room(self.want_play[0], self.want_judge[0], self.number_game)
            self.active_room.append([self.room, self.number_game])
            del self.want_play[0], self.want_judge[0]

    def room_data(self):
        if len(self.active_room) > 0:
            for i in self.active_room:
                i[0].prossesing_dataroom()

    def send_data(self):
        for i in self.users:
            if i.data_get_set:
                i.conn.send(i.data.encode())
                i.data_get_set = False


if __name__ == "__main__":
    server = Server()
    while True:
        try:
            # Подключение к серверу
            server.connect()
        except:
            pass
        try:
            # Получение даты от пользователя
            server.get_data()
        except:
            pass
        # Проверка соединения пользователя
        server.user_errors_connection()

        # Создание игровых комнат если достаточно игроков в поиске
        server.create_room()

        # Обработка даты пользователя внутри комнаты
        server.room_data()

        # -- Отправка даты
        server.send_data()
