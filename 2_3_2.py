# Модификация программы о регулярных выражениях

import re
import data_reg as d


# В магазине
def shop():
    while True:
        ans = input("Вы в магазине. Что Вы будете делать? ").lower()
        # Вернуться
        if re.fullmatch(d.patterns["м_верн"], ans):
            print("Вы вышли из магазина")
            break
        # Осмотреться
        elif re.fullmatch(d.patterns["м_осм"], ans):
            print("Вы видите много людей. "
                  "Сегодня выходной, поэтому многие закупаются "
                  "- предположили Вы.")
        # Выбор
        elif re.fullmatch(d.patterns["м_выбор"], ans):
            print("Вы видите хлеб, молоко и кофемашину. Мда, не густо ...")
        # Взять
        elif re.fullmatch(d.patterns["м_взять"], ans):
            matchs = re.search(d.patterns["м_взять_s"], ans)
            if matchs:
                print(matchs[0])
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
                # !? Недостижимо
                print("Не понятно, что именно вы хотите взять")
        else:
            print("Вы задумались ...")


# Основной цикл
end = False
while not end:
    ans = input("Вы на улице. Ваши действия? ").lower()
    if (re.fullmatch(d.patterns["выход"], ans)):
        # Выход из программы
        print(d.text["gameover"])
        end = True
    elif (re.fullmatch(d.patterns["прогулка"], ans)):
        # На прогулке
        ans = input("Куда именно? (в парк, в супермаркет) ")
        if (re.fullmatch(d.patterns["парк"], ans)):
            print("Вы в парке")
        elif (re.fullmatch(d.patterns["супермаркет"], ans)):
            print("Вы в супермаркете")
        else:
            print("Вы не знаете куда идти")
    elif (re.fullmatch(d.patterns["магазин"], ans)):
        shop()
