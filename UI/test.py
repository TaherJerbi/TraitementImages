from tkinter import *
from PIL import ImageTk,Image
root = Tk()
root.geometry("1000x600")
root.title("Testing app")
# root.iconbitmap("url/name.ico")

def clicked():
    Label(root, text="I clicked").pack()
    btn1['state'] = DISABLED


myLabel2 = Label(root, text="Hello Me!").pack()
btn1 = Button(root, text="Click me !", padx=50, pady=10, command=clicked,fg="blue",bg="white")
btn1.pack()
btnQuit=Button(root,text="bye",command=root.quit)
btnQuit.pack()
myImg=ImageTk.PhotoImage(Image.open("UI/chat.pgm"))
label =Label(image=myImg)
label.pack()
root.mainloop()
#Label Button Entry:input Text:TeextArea Frame:div checkbox  scrollbar
# Displaying a Yes/No Dialog – show you how to use the askyesno() function to display a yes/no dialog.
# Display an OK/Cancel Dialog – show you how to use the askokcancel() function to display an OK/Cancel dialog.
#Show an Open File Dialog – display an open file dialog to allow users to select one or more files.
# tkinter menu for dropdowns
# # tkinter menubutton for dropdowns