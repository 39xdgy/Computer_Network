from tkinter import *
from tkinter import messagebox
import tkinter as Tkinter
from tkinter import filedialog

root = Tkinter.Tk()

def showMessageDialog(header, message):
    messagebox.showinfo( header, message)
    

def startStopCallBack():
    showMessageDialog( "Error", "Not implemented yet")
    try:
        pass
        
    except:
        showMessageDialog( "Some error occured ...")
        return 
    
    
def messageCallBack(event):            
    showMessageDialog( "Error", "Not implemented yet")    



frame = Frame(root)
frame.pack()

root.title("Group chat client application")
root.geometry("800x800")


L1 = Label(root, text="Type a nickname and click start:", font = ('Helvetica', 12, 'normal'))
L1.pack()
L1.place(relx = 0.02,rely = 0.02)
nickText = StringVar()
nickEntry = Entry(root, bd =5,textvariable = nickText)
nickEntry.pack()
nickEntry.place(relwidth=0.35,relx = 0.02,rely = 0.052)

startStopButton = Tkinter.Button(root, text ="Start", font = ('Helvetica', 13, 'bold'),fg = "green", background = "white", activebackground = "red",command = startStopCallBack)
startStopButton.pack()
startStopButton.place(bordermode=OUTSIDE, relheight = 0.065, relwidth=0.15, relx = 0.375, rely = 0.02)

statusLabelText = StringVar()
label = Label( root, textvariable=statusLabelText, font = ('Helvetica', 12, 'normal'),fg = "blue" )
statusLabelText.set("Client is not running.")
label.pack()
label.place(relx = 0.02,rely = 0.12)

scrollbar = Scrollbar(root)
scrollbar.pack()
scrollbar.place(relheight = 0.71,relwidth=0.96, relx = 0.02, rely = 0.15)

   
messageText = Text(root, yscrollcommand = scrollbar.set, font = ('Helvetica', 12, 'normal'))
messageText.insert(END, "Messages from server should appear here.")
messageText.pack()
messageText.place(relheight = 0.70,relwidth=0.94, relx = 0.02, rely = 0.17)
messageText.config(state=DISABLED)
scrollbar.config( command = messageText.yview )
    

L2 = Label(root, text="Type you message and press Enter:", font = ('Helvetica', 12, 'normal'))
L2.pack()
L2.place(relx = 0.02,rely = 0.88)
message = StringVar()
messageEntry = Entry(root, bd =5,textvariable = message)
messageEntry.pack()
messageEntry.bind("<Return>", messageCallBack)
messageEntry.place(relwidth=0.94,relheight = 0.05, relx = 0.02,rely = 0.92)







root.mainloop()