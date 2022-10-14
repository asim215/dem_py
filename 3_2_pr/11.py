# Занятие 11. Словари

# Задача «Номер появления слова»
# Условие
# В единственной строке записан текст. Для каждого слова из данного текста
# подсчитайте, сколько раз оно встречалось в этом тексте ранее.
# Словом считается последовательность непробельных символов идущих подряд,
# слова разделены одним или большим числом пробелов или символами конца строки.
def t1():
    d_a = {}
    for w in input().split():
        if w in d_a.keys():
            d_a[w] += 1
        else:
            d_a[w] = 0
        print(str(d_a[w]), end=' ')


# Задача «Словарь синонимов»
# Условие
# Вам дан словарь, состоящий из пар слов. Каждое слово является синонимом
# к парному ему слову. Все слова в словаре различны.
# Для слова из словаря, записанного в последней строке, определите его синоним.
def t2():
    n = int(input())
    d_syn = dict([input().split() for _ in range(n)])
    s = input()
    if s in d_syn.keys():
        print(d_syn[s])
    elif s in d_syn.values():
        for key, val in d_syn.items():
            if val == s:
                print(key)
    else:
        print("Word doesn't have synonym in dict")


# Задача «Самое частое слово»
# Условие
# Дан текст: в первой строке задано число строк, далее идут сами строки.
# Выведите слово, которое в этом тексте встречается чаще всего. Если таких
# слов несколько, выведите то, которое меньше в лексикографическом порядке.
def readline(f) -> str:
    return f.readline()


def t3(f):
    n = int(readline(f))
    text_li = []
    counter_d = {}
    for _ in range(n):
        text_li += readline(f).split()
    text_s = sorted(text_li)
    for e in text_s:
        if e in counter_d:
            counter_d[e] += 1
        else:
            counter_d[e] = 1
    mk, mv = "", 0
    for k, v in counter_d.items():
        if v > mv:
            mk, mv = k, v
    print(mk)


def t3_fin():
    text_li = []
    counter_d = {}
    for _ in range(int(input())):
        text_li += input().split()
    for e in sorted(text_li):
        if e in counter_d:
            counter_d[e] += 1
        else:
            counter_d[e] = 1
    mk, mv = "", 0
    for k, v in counter_d.items():
        if v > mv:
            mk, mv = k, v
    print(mk)


f = open("input_e.txt", "r")
t3(f)
f.close()
