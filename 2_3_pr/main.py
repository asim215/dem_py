# Модификация программы о регулярных выражениях

import re
import random

import data_reg as d


# Выбор случайного ответа
def get_rand(key):
    return random.choice(d.text[key])


# Проверка всех вариантов по ключу
def check_all(key, text):
    for val in d.patterns[key]:
        res = re.fullmatch(val, text)
        if res:
            return res
    return None


# В магазине
def shop():
    while True:
        ans = input("Вы в магазине. Что Вы будете делать? ").lower()
        # Вернуться
        if check_all("м_верн", ans):
            print("Вы вышли из магазина")
            break
        # Осмотреться
        elif check_all("м_осм", ans):
            print("Вы видите много людей. "
                  "Сегодня выходной, поэтому многие закупаются "
                  "- предположили Вы.")
        # Выбор
        elif check_all("м_выбор", ans):
            print("Вы видите хлеб, молоко и кофемашину. Мда, не густо ...")
        # Взять
        elif check_all("м_взять", ans):
            # matchs = re.search(d.patterns["м_взять_s"], ans)
            matchs = check_all("м_взять_s", ans)
            if matchs:
                if re.fullmatch(".*хлеб.*", matchs[0]):
                    print("Взятие хлеба успешно")
                elif re.fullmatch(".*молоко.*", matchs[0]):
                    print("Пакет молока порвался. Вы сообщили об этом"
                          " сотруднику магазина")
                elif re.fullmatch(".*кофемашин.*", matchs[0]):
                    print("Кофемашина оказалась очень тяжелой."
                          " Вы потянули спину")
                else:
                    print("Не могу ", matchs[0], ". Этого нет на полке")
            else:
                # ! Недостижимо
                print("Не понятно, что именно вы хотите взять")
        else:
            print(get_rand("nothing"))


# Основной цикл
end = False
while not end:
    ans = input("Вы на улице. Ваши действия? ").lower()
    if check_all("выход", ans):
        # Выход из программы
        print(get_rand("gameover"))
        end = True
    elif check_all("прогулка", ans):
        # На прогулке
        ans = input("Куда именно? (в парк, в супермаркет) ")
        if check_all("парк", ans):
            print("Вы в парке")
        elif check_all("супермаркет", ans):
            print("Вы в супермаркете")
        else:
            print("Вы не знаете куда идти")
    elif check_all("магазин", ans):
        # В магазин
        shop()
    else:
        # Неясный ответ
        print(get_rand("unclear"))
