import InstagramAPI
import instagram_tools as tools
import time
import random
import sys

# создаем дефолтный конфиг
tools.create_config()

# пользователи, от лица которых надо ставить лайки
# не существует
# 2: "89262894076,qazqazqaz",
# 4: "kuznetsovvladimir,71vova69",

# закрытый профиль
# 2: "granatkindenis,1971vova",
# 3: "lesya_les91,1971vova",
# 6: "Danilmol09,Danilmol09",
# 7: "semitsvetikova1234,qazqazqaz"
# 1: "mondedekristi,1999777ava",
# # 2: "Kriss_w_l,x217eyz7w",
# # 3: "andrevlog,!977642vers!"

auth_data = {
    1: "andrewa374,1q2w3e4r5t", # также используется для сбора инфы для других акков
}

# имя целевого аккаунта - посты которого нужно лайкать
slaveholder_account_name = "serpuhov_ru"

# текущее время
current_time = time.time()

# 2 суток в секундах
two_days_unix_time = 172800

# время с которого начинаем парсить посты, если в конфиге не задан min_timestamp
feed_capture_time = current_time - two_days_unix_time

# количество аккаунтов
acc_count = len(auth_data.items()) + 1 # +1 для последнего акка

# логинимся с одного акка для сбора фида и необходимых метрик с целевого аккаунта
login, pw = auth_data.get(1).split(",")
current_session = InstagramAPI.InstagramAPI(login, pw)
current_session.login()

# получить id целевого аккаунта по его имени
user_id = tools.get_userid_by_username(slaveholder_account_name)

# если в конфиге не задан min_timestamp, то получаем фид страницы за два дня
if tools.get_setting("Bot_settings", "min_timestamp") == "0":
    print("2 days filter")
    feed_as_list = current_session.getTotalUserFeed(user_id, int(feed_capture_time))
# иначе фильтруем фид по min_timestamp из конфига
else:
    print("last post filter")
    feed_as_list = current_session.getTotalUserFeed(user_id, int(tools.get_setting("Bot_settings", "min_timestamp")))

# количество отфильтрованых постов
feed_count = len(feed_as_list)
print(feed_count)

# если есть новые посты с момента последнего запуска скрипта, то работаем дальше
if feed_count != 0:
    # время создания последнего поста
    last_post_time = feed_as_list[0]["taken_at"]

    # логинимся по очереди в каждый аккаунт и лайкаем посты
    for x in range(1, acc_count):
        login, pw = auth_data.get(x).split(",")

        # логин от имени пользователя, который должен ставить лайк
        current_session = InstagramAPI.InstagramAPI(login, pw)
        current_session.login()

        # случайное время ожидания в секундах после лайка поста в заданном диапазоне
        latency = float(random.randrange(3, 10))

        for y in range(0, feed_count):
            post_id = feed_as_list[y]['id']
            current_session.like(post_id)
            time.sleep(latency)
            print(login + " liked post " + post_id + ' ' + str(y))

        # завершаем текущую сессию
        current_session.logout()

    # записываем время создания последнего поста в конфиг
    tools.change_config("Bot_settings", "min_timestamp", str(last_post_time))

# иначе завершаем программу
else:
    sys.exit("No new posts")
