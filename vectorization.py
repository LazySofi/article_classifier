import codecs
import numpy as np
import random
import pickle

categories = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']

dict_file = codecs.open('processed/dictionary.txt', 'r', 'utf_8_sig')

dictionary = []
for line in dict_file:
    line = line[: len(line) - 1]
    dictionary.append(line)


def similar_words(word1, word2, coef = .5):
    if len(word1) == len(word2):
        ch = 0
        n = len(word1)
        zn = 0
        for i in range(n):
            zn += np.sqrt(n-i)
        for i in range(n):
            if word1[i] == word2[i]:
                ch+=np.sqrt(n-i)
        if ch/zn >= coef:
            return True
        else:
            return False
    else:
        return False


def remove_punctuation(word):
    punctuation = ['!', ':', ':', ',', '.', '?', "'", '"', '(', ')', '«', '»', '+', '-', '=', '_', '/', '\\', '|', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    new_word = ''
    for symbol in word:
        if symbol not in punctuation:
            new_word += symbol
    return new_word.lower()


def line2vec(line, dictionary):
    vector = [0] * len(dictionary)

    for word in line.split():
        word = remove_punctuation(word)
        while len(word) > 0 and word[-1] in ['а', "ы", "у", "й", "е", "о", "я", "и", "ь", "ю", "э"]:
            word = word[:-1]

        for d in dictionary:
            if d == word:
                vector[dictionary.index(d)] += 1
    return vector


train_file = codecs.open('news_train.txt', 'r', 'utf_8_sig')

input_vectors = []
outputs = []
counter = 0
for line in train_file:
    counter +=1
    print(counter)

    '''
    if counter % 4 != 0:
        continue
    else:
        print(counter)
    '''

    label, name, content = line.split('\t')

    name += content

    vector = line2vec(name, dictionary)
    output = categories.index(label)

    input_vectors.append(vector)
    outputs.append(output)


test_vectors_i = open('processed/ftest_vectors_input', 'wb')
test_vectors_o = open('processed/ftest_vectors_outputs', 'wb')

for i in input_vectors:
    pickle.dump(i, test_vectors_i)

for i in outputs:
    pickle.dump(i, test_vectors_o)

print('text processed')