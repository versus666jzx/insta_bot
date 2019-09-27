import requests
import configparser
import os


config_path = "config.ini"


def create_config():
    """ Создает файл конфигурации, если его еще нет"""
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.add_section("Bot_settings")
        config.set("Bot_settings", "min_timestamp", "0")

        # записываем параметры в файл настроек
        with open(config_path, "w") as config_file:
            config.write(config_file)


def get_setting(section, setting):
    """ Возвращает значение необходимого параметра из файла конфигурации"""
    create_config()
    config = configparser.ConfigParser()
    config.read(config_path)
    value = config.get(section, setting)
    return value


def change_config(section, setting, value):
    """ Изменяет значение необходимого параметра в конфиге"""
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set(section, setting, value)

    # записываем изменения в файл настроек
    with open(config_path, "w") as config_file:
        config.write(config_file)


def get_mediaid_by_url(url):
    media_id = requests.get("https://api.instagram.com/oembed/?url={}".format(url)).json()['media_id']
    return str(media_id)


def get_userid_by_username(username):
    logging_page_id = requests.get(f"https://www.instagram.com/{username}" + "/?__a=1").json()['logging_page_id']
    user_id = logging_page_id[12:len(logging_page_id)]
    return str(user_id)
