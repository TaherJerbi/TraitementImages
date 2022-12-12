from math import floor
import matplotlib.pyplot as plt

import numpy as np
from numpy import array, int32


def read_pgm(path):
    with open(path, 'rb') as pgmf:
        im = plt.imread(pgmf)
    return im


def moyenneGris(matrice):
    somme = 0
    for i in range(0, matrice.shape[0]):
        for j in range(0, matrice.shape[1]):
            somme += matrice[i][j]

    return somme / (matrice.shape[0] * matrice.shape[1])


def ecartypeGris(matrice):
    somme = 0
    moy = moyenneGris(matrice)
    for i in range(0, matrice.shape[0]):
        for j in range(0, matrice.shape[1]):
            somme += (matrice[i][j] - moy)**2

    return np.sqrt(somme / (matrice.shape[0] * matrice.shape[1]))


def pgmread(filename):

    f = open(filename, 'r')
    # Read header information
    count = 0
    while count < 3:
        line = f.readline()
        if line[0] == '#':  # Ignore comments
            continue
        count = count + 1
        if count == 1:  # Magic num info
            magicNum = line.strip()
            if magicNum != 'P2' and magicNum != 'P5':
                f.close()
                print('Not a valid PGM file')
                exit()
        elif count == 2:  # Width and Height
            [width, height] = (line.strip()).split()
            width = int(width)
            height = int(height)
        elif count == 3:  # Max gray level
            maxVal = int(line.strip())
    # Read pixels information
    img = []
    buf = f.read()
    elem = buf.split()
    if len(elem) != width*height:
        print('Error in number of pixels')
        exit()
    for i in range(height):
        tmpList = []
        for j in range(width):
            tmpList.append(elem[i*width+j])
        img.append(tmpList)
    return (array(img), width, height)


def pgmwrite(img, filename, maxVal=255, magicNum='P2'):
    img = int32(img).tolist()
    f = open(filename + ".pgm", 'w')
    file = open(filename+".txt", "w+")
    content = str(img)
    file.write(content)
    file.close()
    width = 0
    height = 0
    for row in img:
        height = height + 1
        width = len(row)
    f.write(magicNum + '\n')
    f.write(str(width) + ' ' + str(height) + '\n')
    f.write(str(maxVal) + '\n')
    for i in range(height):
        count = 1
        for j in range(width):
            f.write(str(img[i][j]) + ' ')
            if count >= 17:
                # No line should contain gt 70 chars (17*4=68)
                # Max three chars for pixel plus one space
                count = 1
                f.write('\n')
            else:
                count = count + 1
        f.write('\n')
    f.close()


def histo(img):
    arr = np.zeros(256)
    for row in img:
        for num in row:
            arr[num] += 1
    return arr


def cumule(img):
    arr = histo(img)

    arr_cumul = np.zeros(256)
    arr_cumul[0] = arr[0]
    for i in range(1, len(arr_cumul)):

        arr_cumul[i] = arr[i] + arr_cumul[i-1]

    return arr_cumul


# Hc / nb pix
def P_cumule(img, width, height):
    arr_cumul = cumule(img)
    p_cum = []

    for n in arr_cumul:
        p_cum.append(n/(width*height))

    return p_cum


# Floor ( 255 * Pc )
def n1(img, width, height):
    pc = P_cumule(img, width, height)
    n1_arr = []
    for pi in pc:
        n1_arr.append(floor(pi*255))

    return n1_arr


# Heg de i = somme H de j where n1(j) = i
def Heg(img, width, height):
    h_arr = histo(img)
    n1_arr = n1(img, width, height)
    heg_arr = np.zeros(len(h_arr))

    for i in range(len(h_arr)):
        j = n1_arr[i]
        heg_arr[j] += h_arr[i]

    return heg_arr


def convert_img(img):
    n1_arr = n1(img, width=img.shape[0], height=img.shape[1])

    new_im = np.zeros((img.shape[0], img.shape[1]))

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_im[i][j] = n1_arr[img[i][j]]

    return new_im


def contrast(img, x1, y1, x2, y2):
    corresp = np.zeros(256)
    min = np.min(img)
    max = np.max(img)
    for i in range(256):
        if (i <= x1):
            corresp[i] = y1 * (i - min) / (x1 - min)

        if (i > x1 and i <= x2):
            continue

        if (i > x2):
            continue

        if corresp[i] < 0:
            corresp[i] = 0
        if corresp[i] > 255:
            corresp[i] = 255


im = read_pgm("chat.pgm")
new_im = convert_img(img=im)
plt.imshow(new_im)
pgmwrite(filename="chat_equalized", img=new_im)


# print(moyenneGris(im), " : ", ecartypeGris(im))
