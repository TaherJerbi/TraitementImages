from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
# functions


def openImage():
    # filetypes = (
    #     ('text files', '*.txt'),
    #     ('All files', '*.*')
    # )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/')
    image = ImageTk.PhotoImage(Image.open(filename))
    label.configure(image=image)
    label.image = image
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
    # converty taswyraa


def applyFilter():
    selection = "You selected the filter " + \
        str(f.get()) + " With size "+str(nValue.get())
    print(selection)


def applySeuillage():
    selection = "You selected the seuil " + \
        str(seuilType.get()) + " With rgb "+str(rEntry.get()) + \
        str(gEntry.get())+str(bEntry.get())
    print(selection)


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
EgaliserImage = Button(SideBar, width=30, text="Egaliser",
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
noiseButton = Button(SideBar, width=30, text="Ajouter bruit"
                     ).grid(row=10, sticky="W")
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
                           command=applyFilter).grid(row=16, sticky="W")
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
