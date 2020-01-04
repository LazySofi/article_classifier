import codecs
import numpy as np
import random
from copy import deepcopy
from sklearn.ensemble import RandomForestClassifier
import pickle


categories = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']

files = []
for cat in categories:
    files.append(codecs.open('processed/roots_for_{}.txt'.format(cat), 'r', 'utf_8_sig'))

dictionaries = []

a = 0
for f in files:
    cat_n = files.index(f)

    lines = []
    for line in f:
        lines.append(line[:-1].split())

    flag = 0
    dictionary = []
    old_dict_length = 0
    for line in lines:
        if flag >= 11:
            break

        for word in line[1:-1]:
            if word in dictionary:
                continue

            c = 0
            for line2 in lines:
                if word in line2:
                    c+=1
            if c >= 100 and c <= 400:
                dictionary.append(word)
                flag = 0
            #print(c)
        
        print('{}/1200'.format(a), ' ', len(dictionary))
        a+=1

        dictionary = list(dict.fromkeys(dictionary))

        if old_dict_length == len(dictionary):
            flag +=1
        else:
            old_dict_length = len(dictionary)
    
    n = [False] * len(lines)
    for word in dictionary:
        for i in range(len(lines)):
            for word2 in lines[i]:
                if word2 == word:
                    n[i] = True

    ch = 0
    zn = 0
    for a in n:
        zn += 1
        if a:
            ch += 1

    print(categories[cat_n], ': ', int((ch/zn)*100), '%\n')

    
    dictionaries.append(dictionary)

dictionary_list = []
for d in dictionaries:
    dictionary_list.extend(d)

old_dict = {i: dictionary_list.count(i) for i in dictionary_list}

new_dict = {}

for i in old_dict:
    if old_dict[i] < 3:
        new_dict[i] = old_dict[i]
old_dict = new_dict

print(len(old_dict))

dict_file = codecs.open('processed/dictionary.txt', 'w+', 'utf_8_sig')
for i in old_dict:
    dict_file.write(i + '\n')
