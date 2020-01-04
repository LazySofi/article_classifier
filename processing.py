import codecs
import numpy as np


categories = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']


def remove_punctuation(word):
    punctuation = ['!', ':', ':', ',', '.', '?', "'", '"', '(', ')', '«', '»', '+', '-', '=', '_', '/', '\\', '|', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    new_word = ''
    for symbol in word:
        if symbol not in punctuation:
            new_word += symbol
    return new_word.lower()


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


def find_same_root(word, roots):
    
    for root in roots:
        if len(word) >= len(root[0]):
            for i in range(len(word) - len(root[0]) + 1):
                w = word[i : i + len(root[0])]
                if similar_words(w, root[0]):
                    return root[0]
        else:
            for i in range(len(root[0]) - len(word) + 1):
                w = root[0][i : i + len(word)]
                if similar_words(w, word):
                    root[0] = word
                    return word
    roots.append([word, 0])
    return word

def delete_roots(line, roots):

    for root in roots:
        if root[0] not in line.split():
            root[1] += 1
        else:
            root[1] = 0
        
        if root[1] >= 64:
            roots.remove(root)


train = codecs.open('news_train.txt', 'r', 'utf_8_sig')

files = []
for cat in categories:
    files.append(codecs.open('processed/roots_for_{}.txt'.format(cat), 'w+', 'utf_8_sig'))

cat_roots = []
for i in range(len(categories)):
    cat_roots.append([])


number = 0
names_counts = [0]*10
for line in train:
    label, name, content = line.split('\t')

    cat_n = categories.index(label)
    new_name = ''

    name += content 

    #delete_roots(name, cat_roots[cat_n])

    #print('{0}\r'.format(number))
    
    for word in name.split():
        new_word = remove_punctuation(word)
        while len(new_word) > 0 and new_word[-1] in ['а', "ы", "у", "й", "е", "о", "я", "и", "ь", "ю", "э"]:
            new_word = new_word[:-1]

        if len(new_word) >= 3:
            #find_same_root(new_word, cat_roots[cat_n])
            #cat_roots[cat_n].extend([new_word])
            new_name += new_word + ' '
    

    #new_name = remove_punctuation(name)

    number += 1
    print(number)

    if names_counts[cat_n] <= 1200:
        names_counts[cat_n] += 1
        files[cat_n].write(label + '\t' + new_name + '\t' + 'emptyness' '\n')

print('bl')

'''
for i in range(len(categories)):
    #cat_roots[i] = list(dict.fromkeys(cat_roots[i]))
    for word in cat_roots[i]:
        files[i].write(word[0] + '\n')
'''
for i in range(len(categories)):
    files[i].close()
