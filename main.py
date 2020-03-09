""" Домашнее задание к Занятию №3 """
'''
Считать/скопировать текст из файла
'''
#       Вариант с подключением кодеков
# import codecs
# file = codecs.open('text.txt', 'r', encoding='utf-8')
# data = file.read()
# file.close()

import io           # обходим ошибки с кодировкой
with io.open('text.txt', encoding='utf-8') as file:
    data = file.read()
'''
Методами строк очистить текст от знаков препинания
'''
#       Вариант 1
# punct = ['.', ',', ';', '!', '«', '»', ':', '?', '(', ')', '— '] # набор пунктуации для данного текста; избегаем двойных пробелов
# for i in range(len(punct)):
#     data = data.replace(punct[i], '')
# print(data)

import string
punct = string.punctuation.replace('-', '«»—')      # при удалении длинного тире в тексте сохранятся двойные пробелы
#       Вариант 2
data = ''.join(x for x in data if x not in punct)   # через метод join с пустым разделителем
# print(data)
#       Вариант 3
# data = data.translate(data.maketrans('','', punct))  # через метод translate, указывая только deletechars - третий аргумент
# print(data)
'''
Cформировать list со словами (split)
'''
words_raw = data.split()
print('Исходные слова: ', words_raw)
'''
Привести все слова к нижнему регистру (map)
'''
#       Вариант 1: через метод map
words_lower = list(map(lambda x: x.lower(), words_raw))
# при редактировании кода возникает ошибка на words_lower
# можно привести к нижнему регистру каким-то более корреткным методом?
print('Слова в нижнем регистре: ', words_lower)

#       Вариант 2: через метод append
# words_lower = []
# for item in words_raw:
#     words_lower.append(item.lower())
# print(words_lower)

'''
Получить из list пункта 3 dict, ключами которого являются слова, а значениями - их количество появлений в тексте
'''
import collections
dict_light = collections.Counter()
for i in words_lower:
    dict_light[i] += 1
print(dict_light)

#       Вариант короче:
# from collections import Counter
# dict_light = Counter(words_lower)
# print(dict_light)
"""Примечание для себя:
S.count(str, [start],[end])	Возвращает количество непересекающихся вхождений подстроки в диапазоне [начало, конец]
Кажется, подходит для этой цели. Но считает все вхождения служебных частей речи и местоимений: по ним количества завышены.
Метод подходит для подсчёта самостоятельных (длинных) частей речи.

dict_1 = {words_lower[i] : data.lower().count(words_lower[i]) for i in range(len(words_lower))}
print(dict_1)

# frequency = []
# for i in range(len(words_lower)):
#     frequency.append(data.lower().count(words_lower[i]))
# dict_2 = dict(zip(words_lower, frequency))  # zip сшивает элементы списков на каждой итерации
# print(dict_2)
"""

'''
Вывести 5 наиболее часто встречающихся слов (sort), вывести количество разных слов в тексте (set)
'''
def frequency(item):
   return item[1]
list = list(dict_light.items())
list.sort(key = frequency, reverse = True)
print('Пять наиболее часто встречающихся слов в исходном тексте: ', list[:5])

all_words = set(list)
print('Все слова: ', all_words)

print()
'''
PRO: в пункте 2 дополнительно к приведению к нижнему регистру выполнить лемматизацию.
'''
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
""" 
Убираем из текста все служебные слова (предлоги, союзы, частицы и междометия).
Потом приводим слова к начальным формам.
"""
def pos(word, morth=pymorphy2.MorphAnalyzer()):     # возвращает часть речи, к которой относится слово
    return morth.parse(word)[0].tag.POS         # что за индекс в квадратных скобках?
functional_pos = ('INTJ', 'PRCL', 'CONJ', 'PREP')     # служебные (functional parts of speech)
notional_pos = [word for word in words_lower if pos(word) not in functional_pos]    # самостоятельные (notional POS)
print('Только самостоятельные части речи: ', notional_pos)

list_lemm = []
for i in range(len(notional_pos)):
    razbor = morph.parse(notional_pos[i])[0].normal_form    # приведение слов к начальной форме
    list_lemm.append(razbor)
list_lemm.sort()
print('Только слова в начальной форме: ', list_lemm)

from collections import Counter
dict_pro = Counter(list_lemm)
print(dict_pro)
print('Пять наиболее часто встречающихся самостоятельных слов: ', dict_pro.most_common(5))

"""
Примечания:
После лемматизации наиболее популярными остаются местоимения и глагол "быть".
Из существительных в пятёрку вошла только "жена".
Анализатор pymorphy2 ожидаемо допускает ошибки в приведении к начальной форме имен собственных ('облонской', 'аркадьй').
Глаголы совершенные и несовершенные различает как отдельные формы (наример, 'вспоминать' и 'вспомнить') - следует учесть.
Проблема возникает при оределении начальной формы "мучало" --> "мучалый". Видимо, из-за спряжения.
Правильные обе формы: и "мучить", и "мучать".
"""