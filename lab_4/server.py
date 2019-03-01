import socket



class server:
    def __init__(self):
        self.Port = 62
        self.Buffer_size = 1024
        self.client_list = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', self.Port))
        self.run()

    def run(self):
        while(True):
            message, client_tuple = self.s.recvfrom(self.Buffer_size)
            message = message.decode("utf-8")

            if not client_tuple in self.client_list:
                self.client_list[client_tuple] = message
                print(message)
                for i in self.client_list:
                    intro = message + " is joined into the Chat Room. "
                    self.s.sendto(intro.encode(), i)

            else:
                nick_name = self.client_list[client_tuple]
                for i in self.client_list:
                    send_message = nick_name + ": " + message
                    self.s.sendto(send_message.encode(), i)


if __name__ == "__main__":
    test = server()
