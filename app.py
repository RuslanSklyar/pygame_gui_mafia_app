import pygame
import drawing
from client import Client

# Константы
FPS = 60  # Клово фпс

# Инициализация модуля pygame
pygame.init()

# Main окно
window = pygame.display.set_mode((1920, 1000), pygame.FULLSCREEN)
pygame.display.set_caption("Polemicagame.com")
clock = pygame.time.Clock()

# Модуль отрисовки
draw = drawing.Drawing(window)

# Модуль клиентской части
client_data = Client(drawing.client_api)


# Основное приложение
def main_start_game():
    first_name_singin = "Никнейм/E-mail"
    first_name_singup = "Никнейм"
    e_mail = "E-mail"
    password_1 = "Пароль"
    password_2 = "Повторите пароль"
    inpute_code = ""
    drawing.window_see["sing_in"] = True
    # Основной цикл приложения
    while True:
        window.fill((0, 0, 0))

        client_data.send()  # Отправка data на сервер
        server_data = client_data.get()  # Получение дата с сервера
        draw.data = server_data

        # Цикл обработки событий
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:

                mouse_pos = pygame.mouse.get_pos()
                drawing.mouse_pos_ = mouse_pos
                drawing.use_click = True

                # ----==== Страница входа ====----
                if drawing.window_see["sing_in"]:
                    if (1125 >= mouse_pos[0] >= 795) and (475 >= mouse_pos[1] >= 420):
                        drawing.input_active["first_name"] = True
                        if first_name_singin == "Никнейм/E-mail":
                            first_name_singin = ""
                    else:
                        drawing.input_active["first_name"] = False
                        if len(first_name_singin) == 0:
                            first_name_singin = "Никнейм/E-mail"
                    if (1125 >= mouse_pos[0] >= 795) and (540 >= mouse_pos[1] >= 490):
                        drawing.input_active["password_1"] = True
                        if password_1 == "Пароль":
                            password_1 = ""
                    else:
                        drawing.input_active["password_1"] = False
                        if len(password_1) == 0:
                            password_1 = "Пароль"

                # ----==== Страница регистрации ====----
                if drawing.window_see["sing_up"]:
                    if (1225 >= mouse_pos[0] >= 695) and (370 >= mouse_pos[1] >= 320):
                        drawing.input_active["first_name"] = True
                        if first_name_singup == "Никнейм":
                            first_name_singup = ""
                    else:
                        drawing.input_active["first_name"] = False
                        if len(first_name_singup) == 0:
                            first_name_singup = "Никнейм"
                    if (1225 >= mouse_pos[0] >= 695) and (440 >= mouse_pos[1] >= 390):
                        drawing.input_active["e_mail"] = True
                        if e_mail == "E-mail":
                            e_mail = ""
                    else:
                        drawing.input_active["e_mail"] = False
                        if len(e_mail) == 0:
                            e_mail = "E-mail"

                    if (1225 >= mouse_pos[0] >= 695) and (510 >= mouse_pos[1] >= 460):
                        drawing.input_active["password_1"] = True
                        if password_1 == "Пароль":
                            password_1 = ""
                    else:
                        drawing.input_active["password_1"] = False
                        if len(password_1) == 0:
                            password_1 = "Пароль"

                    if (1225 >= mouse_pos[0] >= 695) and (580 >= mouse_pos[1] >= 530):
                        drawing.input_active["password_2"] = True
                        if password_2 == "Повторите пароль":
                            password_2 = ""
                    else:
                        drawing.input_active["password_2"] = False
                        if len(password_2) == 0:
                            password_2 = "Повторите пароль"

                # ----==== Страница родтверждения когда с e-mail ====----
                if drawing.window_see["inpute_code"]:
                    if (1045 >= mouse_pos[0] >= 870) and (560 >= mouse_pos[1] >= 420):
                        drawing.input_active["inpute_code"] = True
                    else:
                        drawing.input_active["inpute_code"] = False

            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_TAB or i.key == 1073741912 or \
                        (pygame.key.get_mods() & pygame.KMOD_LCTRL) or i.key == pygame.K_RETURN:
                    continue

                if drawing.input_active["inpute_code"]:
                    if i.key == pygame.K_BACKSPACE:
                        inpute_code = inpute_code[:-1]
                    else:
                        if i.unicode in str([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]):
                            if len(inpute_code) < 5:
                                inpute_code += i.unicode
                                drawing.client_api["sing_up"]["inpute_code"] = inpute_code

                if drawing.input_active["first_name"]:
                    if i.key == pygame.K_BACKSPACE:
                        if drawing.window_see["sing_up"]:
                            first_name_singup = first_name_singup[:-1]
                        else:
                            first_name_singin = first_name_singin[:-1]
                    else:
                        if drawing.window_see["sing_up"]:
                            first_name_singup += i.unicode
                        else:
                            first_name_singin += i.unicode

                    if drawing.client_api["window_see"]["sing_in"]:
                        drawing.client_api["sing_in"]["login"] = first_name_singin

                    elif drawing.client_api["window_see"]["sing_up"]:
                        drawing.client_api["sing_up"]["login"] = first_name_singup

                if drawing.input_active["password_1"]:
                    if i.key == pygame.K_BACKSPACE:
                        password_1 = password_1[:-1]
                    else:
                        password_1 += i.unicode

                    if drawing.client_api["window_see"]["sing_in"]:
                        drawing.client_api["sing_in"]["password"] = password_1

                    elif drawing.client_api["window_see"]["sing_up"]:
                        drawing.client_api["sing_up"]["password_1"] = password_1

                if drawing.input_active["password_2"]:
                    if i.key == pygame.K_BACKSPACE:
                        password_2 = password_2[:-1]
                    else:
                        password_2 += i.unicode

                    drawing.client_api["sing_up"]["password_2"] = password_2

                if drawing.input_active["e_mail"]:
                    if i.key == pygame.K_BACKSPACE:
                        e_mail = e_mail[:-1]
                    else:
                        e_mail += i.unicode

                    drawing.client_api["sing_up"]["e_mail"] = e_mail

        # Основная отрисока окн:

        # Окно "Вход"
        if drawing.window_see["sing_in"]:
            draw.first_name_singin = first_name_singin
            draw.password_1 = password_1
            draw.sing_in()

        # Окно "Регистрация"
        elif drawing.window_see["sing_up"]:
            draw.first_name_singup = first_name_singup
            draw.e_mail = e_mail
            draw.password_1 = password_1
            draw.password_2 = password_2
            draw.sing_up()

        # Окно "Ввод кода подтверждения с e-mail"
        elif drawing.window_see["inpute_code"]:
            draw.inpute_code()
            draw.inpute_code_ = inpute_code

        # Окно "основное меню" для поиска игроков
        elif drawing.window_see["main_menu"]:
            draw.main_menu()
            if server_data["window_see"]["lobby_room"] and server_data["window_see"]["main_menu"]:
                draw.lobby_room()

        # Окно "Игровая комната"
        elif drawing.window_see["lobby_room"]:
            draw.lobby_room()

        draw.topbar()
        # кло-во фпс
        clock.tick(FPS)
        pygame.display.set_caption(str(clock.get_fps()))

        pygame.display.update()


if __name__ == "__main__":
    main_start_game()
