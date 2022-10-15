import matplotlib.pyplot as plt

import numpy as np
from numpy import array, int32
def read_pgm(path):
    with open(path, 'rb') as pgmf:
        im = plt.imread(pgmf)
    return im

def moyenneGris(matrice) : 
    somme = 0
    for i in range(0,matrice.shape[0]) :
        for j in range(0,matrice.shape[1]): 
            somme += matrice[i][j]
    
    return somme / (matrice.shape[0] * matrice.shape[1])

def ecartypeGris(matrice) :
    somme = 0
    moy = moyenneGris(matrice)
    for i in range(0,matrice.shape[0]) :
        for j in range(0,matrice.shape[1]): 
            somme += (matrice[i][j]- moy)**2
    
    return np.sqrt(somme / (matrice.shape[0] * matrice.shape[1]))
def pgmread(filename):
 
  f = open(filename,'r')
  # Read header information
  count = 0
  while count < 3:
    line = f.readline()
    if line[0] == '#': # Ignore comments
      continue
    count = count + 1
    if count == 1: # Magic num info
      magicNum = line.strip()
      if magicNum != 'P2' and magicNum != 'P5':
        f.close()
        print('Not a valid PGM file')
        exit()
    elif count == 2: # Width and Height
      [width, height] = (line.strip()).split()
      width = int(width)
      height = int(height)
    elif count == 3: # Max gray level
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
  f = open(filename + ".pgm",'w')
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
    for el in img:
        for num in el:
            arr[num]+=1;
    return arr

def cumule(img):
    arr = histo(img)
    arr_cumul = np.zeros(256)
    somm = 0
    for i,el in enumerate(arr):
        somm += el
        arr[i] = somm
    return arr_cumul



im = read_pgm("zoo.txt")
pgmwrite(filename="out.pgm",img=im)
print(moyenneGris(im), " : ", ecartypeGris(im))
