from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from math import floor
import matplotlib.pyplot as plt

import numpy as np
from numpy import array, int32
import random
# functions

image_stack = []
def addNoise(img):
    new_im = np.zeros((img.shape[0], img.shape[1]))

    for i in range(0, img.shape[0]):
        for j in range(0,img.shape[1]):
            rand = random.randint(0,20)
            if rand == 0:
                new_im[i][j] = 0
            elif rand == 20:
                new_im[i][j] = 255
            else:
                new_im[i][j] = img[i][j]
    return new_im
def filtreMoy(n):
    filtre = np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            filtre[i][j] = 1.0/n
    return filtre
    
def applyFilter(img, filtre): 
    n = filtre.shape[0]
    print("Applying filter : \n", filtre)
    new_im = np.zeros((img.shape[0], img.shape[1]))
    for i in range(0, img.shape[0]):
        for j in range(0,img.shape[1]):
            if i < n//2 or j < n//2 or i > img.shape[0] - n//2 - 1 or j > img.shape[1] - n//2 - 1:
                new_im[i,j] = img[i,j]
            else:
                window = img[i - n//2 : i + n//2 +1, j - n//2 : j + n//2 +1]
                output = np.sum(window * filtre)
                new_im[i,j] = output
    return new_im
    
def applyFiltreMoy(img, n): 
    new_im = applyFilter(img, filtreMoy(n))
    return new_im
def applyMedianFilter(img, n):
    new_im = np.zeros((img.shape[0], img.shape[1]))
    for i in range(0, img.shape[0]):
        for j in range(0,img.shape[1]):
            if i < n//2 or j < n//2 or i > img.shape[0] - n//2 - 1 or j > img.shape[1] - n//2 - 1:
                new_im[i,j] = img[i,j]
            else:
                window = img[i - n//2 : i + n//2 +1, j - n//2 : j + n//2 +1]
                output = np.median(window)
                new_im[i,j] = output
    return new_im

def show_img(image):
    plt.imshow(image)
    plt.show()

def push_image(array):
    image_stack.append(array)
    set_image(array)

def tk_show_image(array):
    img =  ImageTk.PhotoImage(image=Image.fromarray(array))

    canvas = Canvas(root,width=300,height=300)
    canvas.pack()
    canvas.create_image(20,20, anchor="nw", image=img)



def im_read(path):
    with open(path, 'rb') as pgmf:
        im = plt.imread(pgmf)
    return im

def set_image(array):
    image = ImageTk.PhotoImage(Image.fromarray(array.astype(np.uint8)))
    label.configure(image=image)
    label.image = image

def undo():
    global image_stack
    if len(image_stack) <= 1:
        return
    
    image_stack.pop()
    print(len(image_stack))
    set_image(image_stack[-1])
def filtrePasseHaut(n):
    filtre = np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            if i == n//2 and j == n//2:
                filtre[i,j] = n**2
            else:
                filtre[i,j] = -1
    return filtre


def applyRehausser(img, n):
    filtre = filtrePasseHaut(n)
    return applyFilter(img, filtre)
def histo(img):
    arr = np.zeros(256)
    for row in img:
        for num in row:
            arr[int(num)] += 1
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


def egaliser(img):
    n1_arr = n1(img, width=img.shape[0], height=img.shape[1])

    new_im = np.zeros((img.shape[0], img.shape[1]))

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_im[i][j] = n1_arr[int(img[i][j])]

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

def openImage():
    # filetypes = (
    #     ('text files', '*.txt'),
    #     ('All files', '*.*')
    # )
    filename = fd.askopenfilename(
        title='Open a file')
    image_array = im_read(filename)
    push_image(image_array)
    # read image


def saveChanges():
    # write image
    print("Saved")


def calculerInfo():
    # calculer hadoukom
    moyenne = 15
    ecart = 17
    moyLabel["text"] = "Moyenne : "+str(moyenne)
    ecartLabel["text"] = "Ecart type : "+str(ecart)


def applyContrast():
    x1 = x1Entry.get()
    x2 = x2Entry.get()
    y1 = y1Entry.get()
    y2 = y2Entry.get()
    print(x1, x2, y1, y2)
    image_array = contrast(rgb2gray( image_stack[-1]),int(x1), int(y1), int(x2), int(y2))
    push_image(image_array)
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def applyFilterClick():
    selection = "You selected the filter " + \
        str(f.get()) + " With size "+str(nValue.get())
    
    if f.get() == 1:
        image_array = applyFiltreMoy(rgb2gray(image_stack[-1]),int(nValue.get()))
        push_image(image_array)
    
    if f.get() == 2:
        image_array = applyMedianFilter(rgb2gray(image_stack[-1]),int(nValue.get()))
        push_image(image_array)
    
    if f.get() == 3:
        image_array = applyRehausser(rgb2gray(image_stack[-1]),int(nValue.get()))
        push_image(image_array)


    print(selection)



def seuiller(img,r,g,b):
    new_image = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # r
            if img[i][j][0] > r:
                new_image[i][j][0] = 255
            else:
                new_image[i][j][0] = 0
            # g
            if img[i][j][1] > g:
                new_image[i][j][1] = 255
            else:
                new_image[i][j][1] = 0

            #b
            if img[i][j][2] > b:
                new_image[i][j][2] = 255
            else:
                new_image[i][j][2] = 0

    return new_image
def seuiller_ET(img, r, g, b):
    new_image = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # r
            if img[i][j][0] > r and img[i][j][1] > g and img[i][j][2] > b:
                new_image[i][j][0] = 255
                new_image[i][j][1] = 255
                new_image[i][j][2] = 255
            else:
                new_image[i][j][0] = 0
                new_image[i][j][1] = 0
                new_image[i][j][2] = 0
            
    return new_image
def seuiller_OU(img, r, g, b):
    new_image = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # r
            if img[i][j][0] > r or img[i][j][1] > g or img[i][j][2] > b:
                new_image[i][j][0] = 255
                new_image[i][j][1] = 255
                new_image[i][j][2] = 255
            else:
                new_image[i][j][0] = 0
                new_image[i][j][1] = 0
                new_image[i][j][2] = 0
            
    return new_image
def applySeuillage():
    global image_stack
    selection = "You selected the seuil " + \
        str(seuilType.get()) + " With rgb "+str(rEntry.get()) + \
        str(gEntry.get())+str(bEntry.get())
    print(selection)

    if seuilType.get() is 1:    
        image_array = seuiller(image_stack[-1], int(rEntry.get()), int(gEntry.get()), int(bEntry.get()))

        push_image(image_array) 
    if seuilType.get() is 2:    
        image_array = seuiller_ET(image_stack[-1], int(rEntry.get()), int(gEntry.get()), int(bEntry.get()))


        push_image(image_array) 
    if seuilType.get() is 3:    
        image_array = seuiller_OU(image_stack[-1], int(rEntry.get()), int(gEntry.get()), int(bEntry.get()))


        push_image(image_array) 



def egaliserClick():
    print("egaliser")
    image_array = egaliser(rgb2gray(image_stack[-1]))
    push_image(image_array)

def bruitCick():
    print("bruit")
    image_array = addNoise(rgb2gray(image_stack[-1]))
    push_image(image_array) 

root = Tk()
root.geometry("1100x600")
root.title("Editeur image")
root.configure(bg='#DBDBDB')
f = IntVar()
seuilType = IntVar()

# root.iconbitmap("url/name.ico") nhottou icona
# Layout
ImageView = Frame(root, bg='#DBDBDB', width=700, height=600)
ImageView.pack(fill="both", expand=True, side=LEFT)
SideBar = Frame(root, bg="#6B6E70", width=400, height=600, padx=10, pady=20)
SideBar.pack(fill="both", expand=True, side=RIGHT)
# Image view
label = Label(ImageView, bg="#DBDBDB")
label.place(relx=0.5, rely=0.5, anchor=CENTER)
# Sidebar buttons
openImageButton = Button(SideBar, width=30, text="ouvrir image",
                         command=openImage).grid(row=0, sticky="W")

saveChangesButton = Button(SideBar, width=30, text="Enregistrer modifications",
                           command=saveChanges).grid(row=1, sticky="W")
#Calculer moyenne et ecart type
moyLabel = Label(SideBar, text="Moyenne : -", bg="#6B6E70", fg="white")
moyLabel.grid(row=2, sticky="W")
ecartLabel = Label(SideBar, text="Ecart type : -", bg="#6B6E70", fg="white")
ecartLabel.grid(row=3, sticky="W")
CalculateInfo = Button(SideBar, width=30, text="Calculer",
                       command=calculerInfo).grid(row=4, sticky="W")
#Egaliser
EgaliserImage = Button(SideBar, width=30, text="Egaliser",command=egaliserClick
                       ).grid(row=5, sticky="W")
# contraste
Label(SideBar, text="Changer contraste", bg="#6B6E70",
      fg="white").grid(row=6, sticky="W")
pointsFrame = Frame(SideBar, bg="#6B6E70", pady=5)
pointsFrame.grid(row=7, sticky="W")
Label(pointsFrame, text="x:", bg="#6B6E70",
      fg="white").grid(row=1, column=0, sticky="W")
x1Entry = Entry(pointsFrame)
x1Entry.grid(row=1, column=1, sticky="W")
x2Entry = Entry(pointsFrame)
x2Entry.grid(row=1, column=2, sticky="W")
Label(pointsFrame, text="y:", bg="#6B6E70",
      fg="white").grid(row=2, column=0, sticky="W")
y1Entry = Entry(pointsFrame)
y1Entry.grid(row=2, column=1, sticky="W")
y2Entry = Entry(pointsFrame)
y2Entry.grid(row=2, column=2, sticky="W")
ContrastImage = Button(SideBar, width=30, text="Appliquer",
                       command=applyContrast).grid(row=9, sticky="W")
# bruit
noiseButton = Button(SideBar, width=30, text="Ajouter bruit", command=bruitCick
                     ).grid(row=10, sticky="W")
undoButton = Button(SideBar, width=30, text="Undo", command=undo).grid(row=1, sticky="W")
# filtre
Label(SideBar, text="Ajouter un filtre de taille :", bg="#6B6E70",
      fg="white").grid(row=11, sticky="W")

nValue = Entry(SideBar)
nValue.grid(row=12, sticky="W")
Radiobutton(SideBar, bg="#6B6E70", variable=f, value=1,
            text="Moyenneur", fg="white").grid(row=13, sticky="W")
Radiobutton(SideBar, bg="#6B6E70", variable=f, value=2,
            text="Mediane", fg="white").grid(row=14, sticky="W")
Radiobutton(SideBar, bg="#6B6E70", variable=f, value=3,
            text="Passe haut", fg="white").grid(row=15, sticky="W")
applyFilterButton = Button(SideBar, width=30, text="Appliquer",
                           command=applyFilterClick).grid(row=16, sticky="W")
# seuillage
Label(SideBar, text="Ajouter un seuillage rgb :", bg="#6B6E70",
      fg="white").grid(row=17, sticky="W")

seuilPoints = Frame(SideBar, bg="#6B6E70", pady=5)
seuilPoints.grid(row=18, sticky="W")
rEntry = Entry(seuilPoints)
rEntry.grid(row=1, column=1, sticky="W")
gEntry = Entry(seuilPoints)
gEntry.grid(row=1, column=2, sticky="W")
bEntry = Entry(seuilPoints)
bEntry.grid(row=1, column=3, sticky="W")


Radiobutton(SideBar, bg="#6B6E70", variable=seuilType, value=1,
            text="Normal", fg="white").grid(row=19, sticky="W")
Radiobutton(SideBar, bg="#6B6E70", variable=seuilType, value=2,
            text="Et", fg="white").grid(row=20, sticky="W")
Radiobutton(SideBar, bg="#6B6E70", variable=seuilType, value=3,
            text="Ou", fg="white").grid(row=21, sticky="W")
applyFilterButton = Button(SideBar, width=30, text="Appliquer",
                           command=applySeuillage).grid(row=22, sticky="W")
root.mainloop()
