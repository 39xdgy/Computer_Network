import socket
import threading
import tkinter
class client:
    
    def __init__(self):
        self.server = 'localhost'
        self.port = 62
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.thread = threading.Thread(target = self.recv_message)#, args = (self  ))
        self.Log_in = tkinter.Tk()
        self.run()
        

    def run(self):
        self.thread.start()
        self.log_in_window()
        while(True):
            message = input("User Input: ")
            self.send_message(message)


    def log_in_window(self):
        title = tkinter.Label(self.Log_in, text = "Please Log In")
        title.pack()
        e1 = tkinter.Entry(self.Log_in, textvariable = tkinter.StringVar())
        e1.pack()
        log_button = tkinter.Button(self.Log_in, text = "Connect", command =lambda: self.log_in(e1.get()))
        log_button.pack(side = tkinter.LEFT)
        self.Log_in.mainloop()


            
    def log_in(self, nickname):
        self.s.sendto(nickname.encode(), (self.server, self.port))
        self.Log_in.destroy()






        
    def send_message(self, message):
        self.s.sendto(message.encode(), (self.server, self.port))
        
    def recv_message(self):
        while(True):
            response, Addr = self.s.recvfrom(1024)
            response = response.decode("utf-8")
            response = "\n" + response
            print(response)



if __name__ == "__main__":
    test = client()
