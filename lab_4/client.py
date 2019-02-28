import socket
import threading

class client:
    
    def __init__(self):
        self.server = 'localhost'
        self.port = 62
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.thread = threading.Thread(target = self.recv_message)#, args = (self  ))
        self.run()
        

    def run(self):
        self.thread.start()
        while(True):
            self.send_message()


    def send_message(self):
        message = input("User Input: ")
        self.s.sendto(message.encode(), (self.server, self.port))
    def recv_message(self):
        while(True):
            response, Addr = self.s.recvfrom(1024)
            response = response.decode("utf-8")
            response = "\n" + response
            print(response)




test = client()
