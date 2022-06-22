import pygame
from webcamera_pygame_camera import Camera
from main_mafia import Player
import random
from threading import Thread
from time import time


card_click = False
cnt_lst = []

use_click = False  # Переменная для проверки, была ли нажата ЛКМ
use_click_card = False
mouse_pos_ = [0, 0]  # Сохраняем позиции мышки для нажатия class'a Button

# Словарь с информацией, нажато ли поле для ввода текста
input_active = {"first_name": False, "e_mail": False, "inpute_code": False, "password_1": False, "password_2": False}
# Словарь с информацией, какое окно открыто у пользователя
window_see = {"sing_in": False, "sing_up": False, "inpute_code": False, "main_menu": False, "lobby_room": False}

# API
client_api = {
    "window_see": window_see,
    "click": 0,
    "sing_in":
        {
            "login": "~FLiN",
            "password": "123454",
            "accept": False
        },
    "sing_up":
        {
            "login": "",
            "e_mail": "",
            "password_1": "",
            "password_2": "",
            "accept": False,
            "inpute_code": "",
            "code": "",
            "inpute_accept": False,
            "window_input": False
        },
    "main_menu":
        {
            "status_player": False,
            "status_judge": False
        },
    "lobby_room":
        {
            "button_start_game": False,
        }
}


# Основная отрисовка
class Drawing:
    def __init__(self, window):
        self.window = window

        self.count = 0

        # Фото иконок кнопок
        self.logo = 'Resurs/Image/Logo/main_logo.jpg'
        self.exit_white = 'Resurs/Image/Logo/exit_white.png'
        self.exit_red = "Resurs/Image/Logo/exit_red.png"
        self.source_settings = "Resurs/Image/Buttons/settings.png"
        self.source_roll_off = "Resurs/Image/Buttons/rols_off.png"
        self.source_roll_on = "Resurs/Image/Buttons/rols_on.png"
        self.source_refresh = "Resurs/Image/Buttons/refresh_camera.png"
        self.source_foll = "Resurs/Image/Buttons/user_foll.png"
        self.exit_lobby = "Resurs/Image/Buttons/exit_lobby.png"
        self.cards = "Resurs/Image/Lobby/Cards.png"
        self.cards_on = "Resurs/Image/Lobby/cards_on.png"
        self.cards_off = "Resurs/Image/Lobby/cards_off.png"

        # Отрисовака введеных данных от пользователя "вход/ругистрация"
        self.first_name_singin = ""
        self.first_name_singup = ""
        self.e_mail = ""
        self.password_1 = ""
        self.password_2 = ""
        self.inpute_code_ = ""

        # data которую отправляет сервер
        self.data = {}

    # проверка data
    def cheker(self):
        if self.data["sing_in"]["accept"]:
            self.main_menu()

        elif self.data["sing_up"]["accept"]:
            window_see["inpute_code"] = True
            code = random.randint(10000, 99999)
            client_api["sing_up"]["code"] = str(code)
            self.inpute_code()

        elif self.data["sing_up"]["inpute_accept"]:
            self.sing_in()

    # --- Верхний бар с кнопкой "закрыть" и логотипом
    def topbar(self):
        pygame.draw.rect(self.window, (255, 255, 255), (0, 0, 1920, 36), 0)
        Text(self.window, "PolemicaGame", 40, 10, "black", 25).draw()

        ButtonImg(self.window, self.logo, 4, 75, 75, (-100, -100), (-50, -50), func=debug_func).draw()

        ButtonImg(self.window, self.exit_white, 0, 1900, 15, (1880, 2000), (0, 35), func=debug_func).draw()

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if (mouse_pos[0] >= 1880) and (mouse_pos[1] <= 35):
            ButtonImg(self.window, self.exit_red, 0, 1900, 15, (1880, 1920), (0, 35), func=debug_func).draw()
            if mouse_click[0]:
                pygame.quit()
                exit()

    #  Страница входа
    def sing_in(self):
        for k, v in window_see.items():
            window_see[k] = False
            if k == "sing_in":
                window_see[k] = True

        if window_see["sing_in"]:
            mouse_pos = pygame.mouse.get_pos()

            self.window_out = pygame.surface.Surface(self.window.get_size(), 0)
            self.window_out.fill((15, 15, 15))

            self.singin = pygame.surface.Surface((400, 400))
            self.singin.fill((32, 32, 32))

            pygame.draw.rect(self.singin, (150, 0, 0), (0, 0, 400, 400), width=5, border_radius=8)

            Text(self.singin, "Войти", 150, 25, "white", 35).draw()
            # Поле для ввода "Логина"
            self.surface = pygame.surface.Surface((330, 120))
            self.surface.fill((32, 32, 32))
            pygame.draw.rect(self.surface, (80, 80, 80), (0, 0, 330, 50), border_radius=8)
            TextInput(self.surface, self.first_name_singin, 0, 0, "white", 20, input_active["first_name"])
            # Поле для ввода "Пароль"
            pygame.draw.rect(self.surface, (80, 80, 80), (0, 70, 330, 50), border_radius=8)
            TextInput(self.surface, self.password_1, 0, 70, "white", 20, input_active["password_1"], coder=True)

            self.singin.blit(self.surface, (35, 80))

            # Смена цвета при наведении на "Забыли пароль"
            if (885 >= mouse_pos[0] >= 795) and (570 >= mouse_pos[1] >= 560):
                Text(self.singin, "Забыли пароль?", 35, 220, [0, 255, 255], 15).draw()
            else:
                Text(self.singin, "Забыли пароль?", 35, 220, "white", 15).draw()
            # Галочка "Запомнить меня"
            if client_api["click"] == 0:
                pygame.draw.rect(self.singin, (0, 255, 255), (220, 215, 20, 20), width=1, border_radius=3)
            else:
                pygame.draw.rect(self.singin, (0, 255, 255), (220, 215, 20, 20), border_radius=3)
            ButtonImg(self.window_out, None, 0, -5, -5, (980, 1000), (555, 575), func=debug_func).draw()
            Text(self.singin, "Запомнить меня", 245, 220, "white", 15).draw()

            # Смена цвета при наведении на "Вход"
            if (1125 >= mouse_pos[0] >= 795) and (650 >= mouse_pos[1] >= 610):
                pygame.draw.rect(self.singin, (0, 255, 255), (35, 270, 330, 40), border_radius=8)
            else:
                pygame.draw.rect(self.singin, (255, 255, 0), (35, 270, 330, 40), border_radius=8)
            ButtonImg(self.window_out, None, 0, -5, -5, (795, 1125), (610, 650), func=self.cheker).draw()
            Text(self.singin, "Войти", 150, 272, "black", 35).draw()

            # Смена цвета при наведении на "Нет аккаунта"
            if (1125 >= mouse_pos[0] >= 955) and (685 >= mouse_pos[1] >= 675):
                Text(self.singin, "Зарегестрировать аккаунт", 195, 335, [0, 255, 255], 13).draw()
            else:
                Text(self.singin, "Зарегестрировать аккаунт", 195, 335, "white", 13).draw()
            ButtonImg(self.window_out, None, 0, -5, -5, (955, 1125), (675, 685), func=self.sing_up).draw()
            Text(self.singin, "Нет аккаунта?", 35, 335, "white", 15).draw()
            pygame.draw.rect(self.singin, "white", (196, 350, 170, 1), border_radius=1)

            self.window_out.blit(self.singin, (self.window.get_size()[0] // 2 - 200,
                                               self.window.get_size()[1] // 2 - 200))
            self.window.blit(self.window_out, (0, 0))

    # Страница регистрации
    def sing_up(self):
        for k, v in window_see.items():
            window_see[k] = False
            if k == "sing_up":
                window_see[k] = True

        if window_see["sing_up"]:
            mouse_pos = pygame.mouse.get_pos()

            self.window_out = pygame.surface.Surface(self.window.get_size(), 0)
            self.window_out.fill((15, 15, 15))

            self.singup = pygame.surface.Surface((600, 550))
            self.singup.fill((32, 32, 32))
            pygame.draw.rect(self.singup, (150, 0, 0), (0, 0, 600, 550), width=5, border_radius=8)

            Text(self.singup, "Зарегистрироваться", 125, 25, "white", 35).draw()
            # Поле для ввода "Никнейма"
            self.surface = pygame.surface.Surface((530, 260))
            self.surface.fill((32, 32, 32))
            pygame.draw.rect(self.surface, (80, 80, 80), (0, 0, 530, 50), border_radius=8)
            TextInput(self.surface, self.first_name_singup, 0, 0, "white", 20, input_active["first_name"])
            # Поле для ввода "Email"
            pygame.draw.rect(self.surface, (80, 80, 80), (0, 70, 530, 50), border_radius=8)
            TextInput(self.surface, self.e_mail, 0, 70, "white", 20, input_active["e_mail"])
            # Поле для ввода "Пароля"
            pygame.draw.rect(self.surface, (80, 80, 80), (0, 140, 530, 50), border_radius=8)
            TextInput(self.surface, self.password_1, 0, 140, "white", 20, input_active["password_1"], coder=True)
            # Поле для ввода "Повтор пароля"
            pygame.draw.rect(self.surface, (80, 80, 80), (0, 210, 530, 50), border_radius=8)
            TextInput(self.surface, self.password_2, 0, 210, "white", 20, input_active["password_2"], coder=True)

            self.singup.blit(self.surface, (35, 80))

            # Галочка о принятии "политики"
            if client_api["click"] == 0:
                pygame.draw.rect(self.singup, (0, 255, 255), (35, 360, 20, 20), width=1, border_radius=3)
            else:
                pygame.draw.rect(self.singup, (0, 255, 255), (35, 360, 20, 20), border_radius=3)
            ButtonImg(self.window_out, None, 0, -5, -5, (695, 715), (600, 620), func=debug_func).draw()
            Text(self.singup, "Я согласен с правилами пользовательского соглашения и правилами",
                 75, 360, "white", 14).draw()
            Text(self.singup, "обработки персональных данных", 75,  380, "white", 14).draw()

            if (1225 >= mouse_pos[0] >= 695) and (710 >= mouse_pos[1] >= 660):
                pygame.draw.rect(self.singup, (0, 255, 255), (35, 420, 530, 50), border_radius=8)
            else:
                pygame.draw.rect(self.singup, (255, 255, 0), (35, 420, 530, 50), border_radius=8)
            ButtonImg(self.window_out, None, 0, -5, -5, (695, 1225), (660, 710), func=self.cheker).draw()
            Text(self.singup, "Зарегистрироваться", 125, 430, "black", 35).draw()

            if (1225 >= mouse_pos[0] >= 1070) and (745 >= mouse_pos[1] >= 730):
                Text(self.singup, "Авторизоваться", 410, 490, [0, 255, 255], 20).draw()
            else:
                Text(self.singup, "Авторизоваться", 410, 490, "white", 20).draw()
            ButtonImg(self.window_out, None, 0, -5, -5, (1070, 1225), (730, 745), func=self.sing_in).draw()
            Text(self.singup, "Есть аккаунт?", 35, 490, "white", 20).draw()
            pygame.draw.rect(self.singup, "white", (410, 508, 157, 1), border_radius=1)

            self.window_out.blit(self.singup, (self.window.get_size()[0] // 2 - 300,
                                               self.window.get_size()[1] // 2 - 300))
            self.window.blit(self.window_out, (0, 0))

    # Страница ввода кода подтверждения с e-mail
    def inpute_code(self):
        for k, v in window_see.items():
            window_see[k] = False
            if k == "inpute_code":
                window_see[k] = True

        if window_see["inpute_code"]:
            if self.data["sing_up"]["window_input"]:
                client_api["sing_up"]["window_input"] = True
            mouse_pos = pygame.mouse.get_pos()

            self.window_out = pygame.surface.Surface(self.window.get_size(), 0)
            self.window_out.fill((0, 0, 0))

            self.inpt_code = pygame.surface.Surface((500, 200))
            self.inpt_code.fill((32, 32, 32))
            pygame.draw.rect(self.inpt_code, (150, 0, 0), (0, 0, 500, 200), width=5, border_radius=8)
            Text(self.inpt_code, "Введите код подтверждения отправленый вам на e-mail", 40, 20, "white", 15).draw()
            Text(self.inpt_code, "(проверьте папку спам)", 160, 40, "white", 15).draw()

            pygame.draw.rect(self.inpt_code, (80, 80, 80), (160, 80, 175, 40), border_radius=8)
            TextInput(self.inpt_code, self.inpute_code_, 160, 80, "white", 30, input_active["inpute_code"])

            if (1045 >= mouse_pos[0] >= 870) and (620 >= mouse_pos[1] >= 580):
                pygame.draw.rect(self.inpt_code, (0, 255, 255), (160, 140, 175, 40), border_radius=8)
            else:
                pygame.draw.rect(self.inpt_code, (255, 255, 0), (160, 140, 175, 40), border_radius=8)

            ButtonImg(self.inpt_code, None, 0, -5, -5, (870, 1045), (580, 620), func=self.cheker).draw()
            Text(self.inpt_code, "Подтвердить", 180, 150, "black", 20).draw()

            self.window_out.blit(self.inpt_code, (self.window.get_size()[0] // 2 - 250,
                                                  self.window.get_size()[1] // 2 - 100))
            self.window.blit(self.window_out, (0, 0))

    # Страница основного меню для поиска игроков
    def main_menu(self):
        for k, v in window_see.items():
            window_see[k] = False
            self.count = 0
            if k == "main_menu":
                window_see[k] = True

        if window_see["main_menu"]:
            self.window_out = pygame.surface.Surface(self.window.get_size(), 0)
            self.window_out.fill((0, 0, 0))

            size = (self.window_out.get_size()[0] // 2.2, self.window_out.get_size()[1] // 2)

            pygame.draw.rect(self.window_out, (80, 255, 80), (size[0] - 200, size[1]-150, 550, 80), border_radius=8, width=5)

            if client_api["main_menu"]["status_player"]:
                pygame.draw.rect(self.window_out, (255, 80, 80), (size[0] - 200, size[1], 200, 50), border_radius=8)
            else:
                pygame.draw.rect(self.window_out, (80, 80, 80), (size[0] - 200, size[1], 200, 50), border_radius=8)
            Text(self.window_out, "Player", size[0] - 155, size[1] + 10, "white", 35).draw()
            ButtonImg(self.window_out, None, 0, -5, -5, (670, 870), (540, 590), func=status_player).draw()

            if client_api["main_menu"]["status_judge"]:
                pygame.draw.rect(self.window_out, (255, 80, 80), (size[0] + 150, size[1], 200, 50), border_radius=8)
            else:
                pygame.draw.rect(self.window_out, (80, 80, 80), (size[0] + 150, size[1], 200, 50), border_radius=8)
            Text(self.window_out, "Judge", size[0] + 200, size[1] + 10, "white", 35).draw()
            ButtonImg(self.window_out, None, 0, -5, -5, (1020, 1220), (540, 590), func=status_judge).draw()

            try:
                Text(self.window_out, f'Игроков:{self.data["main_menu"]["len_status_player"]}', size[0] - 180, size[1] - 130, "white", 35).draw()
                Text(self.window_out, f'Судьи:{self.data["main_menu"]["len_status_judge"]}', size[0] + 170, size[1] - 130,
                     "white", 35).draw()
            except:
                pass

            self.window.blit(self.window_out, (0, 0))

    # --- Комната лобби для игры
    def lobby_room(self):
        """Вся отрисовка в лобби"""
        for k, v in window_see.items():
            window_see[k] = False
            if k == "lobby_room":
                window_see[k] = True

        if window_see["lobby_room"] and self.count == 0:
            self.cam = Camera(1)
            self.count = 1

        if window_see["lobby_room"]:
            self.window_out = pygame.surface.Surface(self.window.get_size(), 0)
            self.window_out.fill((15, 15, 15))

            ButtonImg(self.window_out, self.source_settings, 1.35, 770, 1035, (715, 795), (980, 1060),
                      func=settings).draw()
            if client_api["click"] == 0:
                ButtonImg(self.window_out, self.source_roll_off, 1.35, 905, 1035, (850, 930), (980, 1060),
                          func=rols_on_off).draw()
            else:
                ButtonImg(self.window_out, self.source_roll_on, 1.35, 905, 1035, (850, 930), (980, 1060),
                          func=rols_on_off).draw()
            ButtonImg(self.window_out, self.source_refresh, 1.35, 1040, 1035, (985, 1065), (980, 1060),
                      func=refresh).draw()
            ButtonImg(self.window_out, self.source_foll, 1.35, 1173, 1035, (1120, 1200), (980, 1060),
                      func=foll).draw()

            ButtonImg(self.window_out, self.exit_lobby, 2.5, 1885, 110, (1830, 1870), (60, 95),
                      func=start_game).draw()
            pygame.draw.rect(self.window_out, (46, 46, 46), (1700, 58, 120, 37), border_radius=8)
            Text(self.window_out, f"Игра: #0000{self.data['lobby_room']['mafia_api']['mafia_number_game']}", 1715, 70, "white", 15).draw()

            self.name_judge = self.data['lobby_room']['mafia_api']['mafia_players'][0]
            if len(self.name_judge) > 10:
                self.name_judge = self.name_judge[:10] + "..."

            pygame.draw.rect(self.window_out, (46, 46, 46), (35, 58, len(self.name_judge) * 15 + 20, 37), border_radius=8)
            Text(self.window_out, f"Судья: {self.name_judge}", 45, 70, "white", 12).draw()

            pygame.draw.rect(self.window_out, (46, 46, 46), (len(self.name_judge) * 15 + 65, 58, 190, 37), border_radius=8)
            Text(self.window_out, "До смены этапа 60 сек", len(self.name_judge) * 15 + 75, 70, "white", 12).draw()

            # --- Центральное окно информации о стадии игры
            pygame.draw.rect(self.window_out, (32, 32, 32), (810, 470, 320, 55), border_radius=8)
            pygame.draw.rect(self.window_out, (32, 32, 32), (500, 635, 920, 5), border_radius=2)

            if not self.data["lobby_room"]["mafia_api"]["mafia_start_game"]:
                if client_api["main_menu"]["status_judge"]:
                    pygame.draw.rect(self.window_out, (32, 32, 32), (920, 550, 90, 55), border_radius=8)
                    Text(self.window_out, "Start", 940, 570, "white", 20).draw()
                    ButtonImg(self.window_out, None, 0, 0, 0, (920, 1010), (555, 605), func=start_game).draw()

                Text(self.window_out, "Ожидание сбора игроков", 830, 487, "white", 20).draw()
            else:
                # --- Текст
                Text(self.window_out, "День | Речь игрока:", 830, 487, "white", 20).draw()

            Text(self.window_out, "Polemica", self.window_out.get_size()[0] // 2 - 55, 58, "white", 25).draw()

            # --- Камера
            self.window_out.blit(self.cam.start(), (965, 115))  # Box 1
            self.window_out.blit(self.cam.start(), (1430, 115))  # Box 2
            self.window_out.blit(self.cam.start(), (1430, 380))  # Box 3
            self.window_out.blit(self.cam.start(), (1430, 645))  # Box 4
            self.window_out.blit(self.cam.start(), (965, 645))  # Box 5
            self.window_out.blit(self.cam.start(), (500, 645))  # Box 6
            self.window_out.blit(self.cam.start(), (35, 645))  # Box 7
            self.window_out.blit(self.cam.start(), (35, 380))  # Box 8
            self.window_out.blit(self.cam.start(), (35, 115))  # Box 9
            self.window_out.blit(self.cam.start(), (500, 115))  # Box 10

            DrawNickname(self.window_out, "1", "Name 1", 970, 330, [65, 105, 225]).draw()
            DrawNickname(self.window_out, "2", "Name 2",1435, 330, [210, 105, 30]).draw()
            DrawNickname(self.window_out, "3", "Name 3", 1435, 595, [148, 0, 211]).draw()
            DrawNickname(self.window_out, "4", "Name 4", 1435, 860, [250, 128, 114]).draw()
            DrawNickname(self.window_out, "5", "Name 5", 970, 860, [0, 250, 154]).draw()
            DrawNickname(self.window_out, "6", "Name 6", 505, 860, [30, 144, 255]).draw()
            DrawNickname(self.window_out, "7", "Name 7", 40, 860, [255, 0, 255]).draw()
            DrawNickname(self.window_out, "8", "Name 8", 40, 595, [221, 160, 221]).draw()
            DrawNickname(self.window_out, "9", "Name 9", 40, 330, [222, 184, 135]).draw()
            DrawNickname(self.window_out, "10", "Name 10", 505, 330, [50, 205, 50]).draw()

            if use_click_card is not True and self.data["lobby_room"]["mafia_api"]["mafia_start_game"] and client_api["main_menu"]["status_player"]:
                self.window_black = pygame.surface.Surface(self.window_out.get_size(), 0)
                self.window_black.fill((0, 0, 0))
                self.window_black.set_alpha(220)
                self.window_out.blit(self.window_black, (0, 0))

                DrawCards(self.window_out, self.data["lobby_room"]["mafia_api"]["mafia_event"]["mafia_rols"], self.cards_on, self.cards_off).draw()
            else:
                cnt_lst.clear()

            # --- Вывожу отрисовку на главный экран
            self.window.blit(self.window_out, (0, 0))


# --- Класс вывода карт при раздаче на экран
class DrawCards:
    def __init__(self, window, data_cards, source_on, source_off):
        self.window = window
        self.data_cards = data_cards
        self.source_on = source_on
        self.source_off = source_off
        self.card_red = "Resurs/Image/Lobby/cards_red.png"
        self.card_mafia = "Resurs/Image/Lobby/cards_mafia.png"
        self.card_don = "Resurs/Image/Lobby/cards_sherif.png"
        self.card_sherif = "Resurs/Image/Lobby/cards_sherif.png"

    def draw(self):
        global use_click, use_click_card, card_click
        pygame.draw.rect(self.window, (32, 32, 32), (675, 215, 600, 480), border_radius=8)
        Text(self.window, "Выберите карту", 705, 255, "white", 25).draw()
        pos_x_1 = 645
        pos_x_2 = 645
        pos_y_1 = 415
        pos_y_2 = 575
        cnt = -1
        for i in self.data_cards:
            cnt += 1
            if i != "Clear":
                img_button = pygame.image.load(self.source_on).convert_alpha()
            else:
                img_button = pygame.image.load(self.source_off).convert_alpha()

            if cnt <= 4:
                pos_x_1 += 110
                button_rect = img_button.get_rect(center=(pos_x_1, pos_y_1))
            else:
                pos_x_2 += 110
                button_rect = img_button.get_rect(center=(pos_x_2, pos_y_2))

            if pygame.Rect.collidepoint(button_rect, pygame.mouse.get_pos()) and i != "Clear" and use_click:
                self.start_time = time()
                thread = Thread(target=self.timer, args=(1, ))
                thread.start()
                use_click = False
                card_click = True
                cnt_lst.append(cnt)

            if len(cnt_lst) > 0:
                if cnt == cnt_lst[0] and card_click:
                    if self.data_cards[cnt] == "Мирный житель":
                        img_button = pygame.image.load(self.card_red).convert_alpha()
                    elif self.data_cards[cnt] == "Мафия":
                        img_button = pygame.image.load(self.card_mafia).convert_alpha()
                    elif self.data_cards[cnt] == "Дон":
                        img_button = pygame.image.load(self.card_don).convert_alpha()
                    elif self.data_cards[cnt] == "Шериф":
                        img_button = pygame.image.load(self.card_sherif).convert_alpha()

                    if cnt <= 4:
                        button_rect = img_button.get_rect(center=(pos_x_1, pos_y_1))
                    else:
                        button_rect = img_button.get_rect(center=(pos_x_2, pos_y_2))

            self.window.blit(img_button, button_rect)

    def timer(self, g_time):
        global use_click_card, card_click
        run = True
        while run:
            real_time = g_time - round(time() - self.start_time)
            if real_time == 0:
                run = False
                use_click_card = True
                client_api["lobby_room"]["n_card"] = cnt_lst[0]
                card_click = False


# --- Класс вывода текста NickName'a на экран
class DrawNickname:
    def __init__(self, window, box, name, x, y, color):
        self.window = window
        self.name = name
        self.box = box
        self.x = x
        self.y = y
        self.color = color

        if len(self.name) <= 15:
            self.sizename = len(self.name)
        else:
            self.sizename = 15
            self.name = self.name[:15] + "..."

    def draw(self):
        pygame.draw.rect(self.window, self.color, (self.x, self.y, 35, 35), border_radius=4)
        pygame.draw.rect(self.window, [38, 38, 38], (self.x + 45, self.y, self.sizename * 15, 35), border_radius=4)
        Text(self.window, self.name, self.x + 50, self.y + 10, "white", 20).draw()
        if len(self.box) == 1:
            Text(self.window, self.box, self.x + 12, self.y + 10, "white", 20).draw()
        else:
            Text(self.window, self.box, self.x + 6, self.y + 10, "white", 20).draw()


# --- Класс вывода текста на экран
class Text:
    def __init__(self, window, text, x, y, color, size):
        self.window = window
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size

        self.button_font = pygame.font.Font('Resurs/Font/freesansbold.ttf', self.size)

    def draw(self):
        start = self.button_font.render(self.text, bool(1), pygame.Color(self.color))
        self.window.blit(start, (self.x, self.y))


# --- Класс введенного текста от пользователя с выводом на экран
class TextInput:
    def __init__(self, window, text, x, y, color, size, input_active_, coder=False):
        self.window = window
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.coder = coder
        self.size = size
        self.input_active = input_active_

        self.draw()

    def draw(self):
        if self.coder is not True:
            if window_see["sing_in"]:
                if len(self.text) > 30:
                    self.text = self.text[len(self.text) - 30:]
            else:
                if len(self.text) > 40:
                    self.text = self.text[len(self.text) - 40:]

            if window_see["inpute_code"]:
                Text(self.window, f"{self.text}", self.x + 40, self.y + 5, self.color, self.size).draw()
            else:
                Text(self.window, f"{self.text}", self.x + 10, self.y + 15, self.color, self.size).draw()
        else:
            if window_see["sing_in"]:
                if len(self.text) > 38:
                    self.text = self.text[len(self.text) - 38:]
            else:
                if len(self.text) > 55:
                    self.text = self.text[len(self.text) - 55:]
            if self.text == "Пароль" or self.text == "Повторите пароль":
                Text(self.window, f"{self.text}", self.x + 10, self.y + 15, self.color, self.size).draw()
            else:
                Text(self.window, "*" * len(self.text), self.x + 10, self.y + 15, self.color, self.size).draw()

        if self.input_active:
            if window_see["sing_up"]:
                pygame.draw.rect(self.window, (0, 255, 255), (self.x, self.y, 530, 50), border_radius=8, width=3)
            elif window_see["inpute_code"]:
                pygame.draw.rect(self.window, (0, 255, 255), (self.x, self.y, 175, 40), border_radius=8, width=3)
            else:
                pygame.draw.rect(self.window, (0, 255, 255), (self.x, self.y, 330, 50), border_radius=8, width=3)


# --- Класс кнопок
class ButtonImg:
    def __init__(self,  window, source, scale, x, y, cx, cy, func=None):
        self.window = window
        self.source = source
        self.scale = scale
        self.x = x
        self.y = y
        self.cx = cx
        self.cy = cy
        self.func = func

    def draw(self):
        if self.source is not None:
            img_button = pygame.image.load(self.source).convert_alpha()

            if self.scale > 0:
                button_scale = pygame.transform.scale(img_button, (img_button.get_width() //
                                                                   self.scale, img_button.get_height() // self.scale))
                button_rect = img_button.get_rect(center=(self.x, self.y))
                self.window.blit(button_scale, button_rect)
            else:
                button_rect = img_button.get_rect(center=(self.x, self.y))
                self.window.blit(img_button, button_rect)
        self.click()

    def click(self):
        global use_click, mouse_pos_
        if use_click and (self.cx[1] >= mouse_pos_[0] >= self.cx[0]) and (self.cy[1] >= mouse_pos_[1] >= self.cy[0]):
            if window_see["lobby_room"]:
                pygame.draw.rect(self.window, (32, 32, 32), (self.x-55, self.y - 55, 80, 80), border_radius=8, width=4)
            use_click = False
            self.func()


# --- Функции действий
# --- Кнопка "Настройки" = Лобби
def settings():
    print("settings")


# --- Кнопка "Вкл\выкл роли" = Лобби
def rols_on_off():
    if client_api["click"] == 0:
        client_api["click"] = 1
        print("rols on")
    else:
        client_api["click"] = 0
        print("rols off")


# --- Кнопка "Обновить камеру" = Лобби
def refresh():
    print("refresh camera")


# --- Кнопка "Выкрик" = Лобби
def foll():
    g = Player.speak_foll
    print(g)


# --- Кнопка "Микрофон" = Лобби
def microphone():
    print("micro")


# --- Кнопка "Запуск игры" = Лобби
def start_game():
    client_api["lobby_room"]["button_start_game"] = True


# --- Кнопка "Player" = основное меню для поиска игроков
def status_player():
    if client_api["main_menu"]["status_player"]:
        client_api["main_menu"]["status_player"] = False
    else:
        client_api["main_menu"]["status_player"] = True
    client_api["main_menu"]["status_judge"] = False


# --- Кнопка "Judge" = основное меню для поиска судей
def status_judge():
    client_api["main_menu"]["status_player"] = False
    if client_api["main_menu"]["status_judge"]:
        client_api["main_menu"]["status_judge"] = False
    else:
        client_api["main_menu"]["status_judge"] = True


def debug_func():
    if client_api["click"] == 0:
        client_api["click"] = 1
    else:
        client_api["click"] = 0
