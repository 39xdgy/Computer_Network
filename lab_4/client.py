import socket
import threading
import tkinter
class client:
    
    def __init__(self):
        self.server = 'localhost'
        self.port = 75
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Log_in = tkinter.Tk()
        self.chat_room = tkinter.Tk()
        self.ws = self.Log_in.winfo_screenwidth()
        self.hs = self.Log_in.winfo_screenheight()
        self.chat_room.withdraw()
        self.chat_window()
        self.thread = threading.Thread(target = self.recv_message)
        self.run()
        

    def run(self):
        self.thread.start()
        self.log_in_window()


    def log_in_window(self):
        x = self.ws/2 - (256/2)
        y = self.hs/2 - (64-2)
        self.Log_in.geometry("256x64+%d+%d"%(x, y))
        title = tkinter.Label(self.Log_in, text = "Please Log In")
        title.pack()
        e1 = tkinter.Entry(self.Log_in, textvariable = tkinter.StringVar())
        e1.pack()
        log_button = tkinter.Button(self.Log_in, text = "Log In", command =lambda: self.log_in(e1.get()))
        log_button.pack(side = tkinter.BOTTOM)
        self.Log_in.mainloop()


            
    def log_in(self, nickname):
        self.s.sendto(nickname.encode(), (self.server, self.port))
        self.Log_in.destroy()
        self.chat_room.deiconify()

    def chat_window(self):
        x = self.ws/2 - (1024/2)
        y = self.hs/2 - (650/2)
        self.chat_room.geometry("1024x650+%d+%d" % (x, y))
        title = tkinter.Label(self.chat_room, text = "Chat Room")
        title.pack(side = tkinter.TOP)
        
        scrollbar = tkinter.Scrollbar(self.chat_room)
        scrollbar.pack()
        scrollbar.place(relheight = 0.71,relwidth=0.96, relx = 0.02, rely = 0.15)

   
        messageText = tkinter.Text(self.chat_room, yscrollcommand = scrollbar.set, font = ('Helvetica', 12, 'normal'))
        messageText.insert(tkinter.END, "Messages from server should appear here.")
        messageText.pack(side = tkinter.TOP)
        messageText.place(relheight = 0.70,relwidth=0.94, relx = 0.02, rely = 0.17)
        messageText.config(state=tkinter.DISABLED)
        scrollbar.config( command = messageText.yview )
        
        message_box = tkinter.Entry(self.chat_room)
        send_button = tkinter.Button(self.chat_room, text = "Send", command = lambda: self.send_message(message_box.get()))
        send_button.pack(side = tkinter.BOTTOM)
        message_box.pack(side = tkinter.BOTTOM)
        


    def send_message(self, message):
        self.s.sendto(message.encode(), (self.server, self.port))
        
    def recv_message(self):
        while(True):
            response, Addr = self.s.recvfrom(1024)
            response = response.decode("utf-8")
            response = "\n" + response
            print(response)
            
            
            messageText.configure(state = 'normal')
            messageText.insert(tkinter.END, response)
            messageText.configure(state = 'disable')
            messageText.event_generate("<<TextModified>>")
            

if __name__ == "__main__":
    test = client()
