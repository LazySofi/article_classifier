import codecs
import numpy as np
import random
from copy import deepcopy
from sklearn.ensemble import RandomForestClassifier
import pickle


def pickleLoader(pklFile):
    try:
        while True:
            yield pickle.load(pklFile)
    except EOFError:
        pass


categories = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']

dict_file = codecs.open('processed/dictionary.txt', 'r', 'utf_8_sig')

dictionary = []
for line in dict_file:
    line = line[: len(line) - 1]
    dictionary.append(line)

train_vectors_i = open('processed/train_vectors_input', 'rb')
train_vectors_o = open('processed/train_vectors_outputs', 'rb')

input_vectors = []
outputs = []

for line in pickleLoader(train_vectors_i):
    input_vectors.extend([line])

for line in pickleLoader(train_vectors_o):
    outputs.extend([line])

while(len(input_vectors) != len(outputs)):
    input_vectors = input_vectors[:-1]

print('read')

clf = RandomForestClassifier(n_estimators=200, max_features='auto', bootstrap=True, min_samples_split=4)
clf.fit(input_vectors, outputs)

print(clf.score(input_vectors, outputs))

model = codecs.open('proccessed.txt', 'w+', 'utf_8_sig')
model.write(str(clf.get_params()))
model.close()

with open('processed/model', 'wb') as f:
    pickle.dump(clf, f)