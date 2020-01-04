import codecs
import numpy as np
import random
from copy import deepcopy
from sklearn.ensemble import RandomForestClassifier
import pickle

categories = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']

def pickleLoader(pklFile):
    try:
        while True:
            yield pickle.load(pklFile)
    except EOFError:
        pass


with open('processed/model', 'rb') as f:
    clf = pickle.load(f)

test_vectors_i = open('processed/ftest_vectors_input', 'rb')
test_vectors_o = open('processed/ftest_vectors_outputs', 'rb')

input_vectors = []
outputs = []

for line in pickleLoader(test_vectors_i):
    input_vectors.extend([line])

for line in pickleLoader(test_vectors_o):
    outputs.extend([line])

while(len(input_vectors) != len(outputs)):
    input_vectors = input_vectors[:-1]

result_file = codecs.open('processed/result.txt', 'w+', 'utf_8_sig')

outputs = clf.predict(input_vectors)
for output in outputs:
    result_file.write(categories[output] + '\n')
    
