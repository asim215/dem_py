# Модификация программы о регулярных выражениях

import re

# Данные
text = {
    "gameover": "Игра окончена! До свидания.",
}
patterns = {
    "выход": ".*выход|выйт.*",
    "магазин": ".*(идт|напр|передв|пой(д|т)).*магазин.*",
    "м_выбор": ".*(выбир|осматр|подой).*продукт.*",
    "м_осм": ".*осм(о|а)тр.*",
    "м_верн": ".*(вернут|улиц|выйт).*",
    "м_взять": r".*(взять|возьму)\s(\w)+.*",
    "прогулка": ".*гулять.*",
    "парк": ".*парк.*",
    "супермаркет": ".*супермаркет.*",
}


# В магазине
def shop():
    while True:
        ans = input("Вы в магазине. Что Вы будете делать? ").lower()
        # Вернуться
        if re.fullmatch(patterns["м_верн"], ans):
            print("Вы вышли из магазина")
            break
        # Осмотреться
        elif re.fullmatch(patterns["м_осм"], ans):
            print("Вы видите много людей. "
                  "Сегодня выходной, поэтому многие закупаются "
                  "- предположили Вы.")
        # Выбор
        elif re.fullmatch(patterns["м_выбор"], ans):
            print("Вы видите хлеб, молоко и кофемашину. Мда, не густо ...")
        # Взять
        elif re.fullmatch(patterns["м_взять"], ans):
            matchs = re.search(patterns["м_взять"], ans)
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
                print("Не понятно, что именно вы хотите взять")
        else:
            print("Вы задумались ...")


end = False
while not end:
    ans = input("Вы на улице. Ваши действия? ").lower()
    if (re.fullmatch(patterns["выход"], ans)):
        # Выход из программы
        print(text["gameover"])
        end = True
    elif (re.fullmatch(patterns["прогулка"], ans)):
        # На прогулке
        ans = input("Куда именно? (в парк, в супермаркет) ")
        if (re.fullmatch(patterns["парк"], ans)):
            print("Вы в парке")
        elif (re.fullmatch(patterns["супермаркет"], ans)):
            print("Вы в супермаркете")
        else:
            print("Вы не знаете куда идти")
    elif (re.fullmatch(patterns["магазин"], ans)):
        shop()
