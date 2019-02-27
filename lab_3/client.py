import socket
import time

TCP_IP = '127.0.0.1'
TCP_Port = 62
Buffer_Size = 1024


class client:

    def __init__(self):
        self.web_name = []
        

    def add_request(self, website):
        self.web_name.append(website)

    def delete_request(self, website):
        self.web_name.remove(website)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_Port))
        while(True):
            for i in self.web_name:
                #print("inside client infinit loop")
                s.send(i.encode())
                print(s.recv(Buffer_Size).decode("utf-8"))
                time.sleep(3)


if __name__ == "__main__":
    test = client()
    test.add_request("www.google.com")
    test.add_request("www.uiowa.edu")
    test.add_request("www.yahoo.com")
    test.run()
