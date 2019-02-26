import socket

TCP_IP = '127.0.0.1'
TCP_Port = 80
Buffer_size = 1024


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
                s.send(i.encode())
                print(s.recv(Buffer_size))
                time.sleep(30)


if __name__ == "__main__":
    test = client()
    test.add_request("www.google.com")
    test.run()
