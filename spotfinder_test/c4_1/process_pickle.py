#!/home/hbernstein/dials/build/bin/python

import pickle

objects = []
with open('strong.pickle', 'rb') as file:
    while True:
        try:
            objects.append(pickle.load(file))
        except EOFError:
            break

print(objects)
