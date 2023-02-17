#!/usr/bin/env python
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt

time = 10 # czas symulacji
L = 5 # dlugosc boku obrazka
N = L * L # liczba neuronow
n = 2 # liczba wzorcow do nauczenia
one = np.identity(N,dtype = np.int8)
w = np.zeros((N,N),dtype = np.int8)

# wczytywanie obrazka
img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)

# sprawdzanie wymiarów obrazka
if img.shape[0] < L or img.shape[1] < L:
    print("Error: Image is smaller than 5x5")
    sys.exit()

# przycięcie obrazka do 5x5
img = img[:L, :L]

# przekonwertowanie obrazka na czarno-biały
_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# przekonwertowanie obrazka na wartości 1 lub -1
x = (img / 255 * 2) - 1
x = x.flatten()

# print image
print(x.reshape(L,L))

pattern = []
pattern.append(np.array([-1,1,1,1,-1,1,-1,-1,-1,1,1,1,1,1,1,1,-1,-1,-1,1,1,-1,-1,-1,1])) # A
#print(pattern[-1].reshape(L,L))
pattern.append(np.array([1,1,1,1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1,-1,1,1,1,1,1])) # Z
#print(pattern[-1].reshape(L,L))
# etap uczenia
for mu in range(n):
    w += np.outer(pattern[mu],pattern[mu])-one
    #print(w)
# etap symulacji (rozpoznawania wzorca)
for t in range(time):
    if (t % 1 == 0):
        print(t*100/time,"%")
        plt.imshow(x.reshape(L,L), cmap = plt.cm.Greys_r, interpolation = 'none')
        plt.savefig(str('letter%03d' % t)+".png", format="png")
    x = np.sign(np.dot(w,x))
    for i in range(N):
        if(x[i]==0):
            x[i]=1
