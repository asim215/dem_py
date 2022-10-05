import re

print("Вы вышли на улицу. Что вы будете делать?")

while True:
    answer = input()
    if(re.fullmatch(".*откр.*зонт.*",answer)):
        print("Вы забыли зонт дома. Что вы будете делать дальше?")
    elif(re.fullmatch(".*выйт.*",answer)):
        print("Вы вышли от сюда. Досваидания!")
        break
    elif(re.fullmatch(".*гулять.*", answer)):
        while True:
            ans = input("Куда именно? (в парк, в супермаркет)")
            if (re.fullmatch(".*парк.*", ans)):
                print("Вы в парке")
            elif (re.fullmatch(".*супермаркет.*", ans)):
                print("Вы в супермаркете")
            else:
                print("Вы не знаете куда идти")
    elif(re.fullmatch(".*идт|напр|передв|пой(д|т).*магазин.*",answer)):
        print("Вы пришли в магазин. Что вы там будете делать?")
        while True:
            answer = input()
            if(re.fullmatch(".*вернут|улиц|выйти.*",answer)):
                print("Вы снова на улице")
                break
            elif(re.fullmatch(".*выбир|осматр|подой.*продукт.*",answer)):
                print("Вы видите хлеб, молоко и кофемашину. Мда, не густо....")
            elif(re.fullmatch(".*взять\s(\w)+.*",answer)):
                matchs = re.search("взять\s(\w)+",answer)
                if matchs:
                    if(matchs[0] == "взять хлеб"):
                        print("взятие хлеба произошло успешно")
                    elif(matchs[0] == "взять молоко"):
                        print("пакет оказался порван. вы облились")
                    elif(matchs[0] == "взять кофемашину"):
                        print("она слишком тяжелая")
                    else:
                        print("Я не могу ", matchs[0], " этого нет на полке")
                else:
                    print("Не понятно, что именно вы хотите взять")