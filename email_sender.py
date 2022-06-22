import smtplib


def send_email(e_mail_out, message):
    e_mail_login = "flindota2@gmail.com"
    password = "123454Aaaa@"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(e_mail_login, password)
        server.sendmail(e_mail_login, e_mail_out, f"Subject:Аутентификация Mafia Game!\n{message} "
                                                  f"- Ваш код аутентификации")
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main(code, e_mail):
    message = str(code)
    e_mail_out = str(e_mail)
    send_email(e_mail_out, message=message)
