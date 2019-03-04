import socket



class server:
    def __init__(self):
        self.Port = 75
        self.Buffer_size = 1024
        self.client_list = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('', self.Port))
        self.ack = 0
        self.run()

    def run(self):
        while(True):
            self.ack += 1
            message, client_tuple = self.s.recvfrom(self.Buffer_size)
            message = message.decode("utf-8")
            if(message[0:6] == "ACK: {" and message.endswith("}")):
                ack_num = int(message[6:])
                temp_client = {client_tuple : (message, ack_num, True)}
                self.client_list.update(temp_client)
            
            elif not client_tuple in self.client_list:
                self.client_list[client_tuple] = (message, self.ack, True)
                print(message)
                for i in self.client_list:
                    intro = message + " is joined into the Chat Room. "
                    self.s.sendto(intro.encode(), i)

            else:
                nick_name = self.client_list[client_tuple][0]
                for i in self.client_list:
                    ack_num = self.client_list[i][1]
                    if(self.ack - ack_num > 3):
                        temp_client = {i:(self.client_list[i][0], self.client_list[i][1], False)}
                        self.client_list.update(temp_client)
                        print("drop client " + self.client_list[i][0])
                    if(self.client_list[i][2] == True):
                        send_message = nick_name + ": " + message
                        send_message = send_message + "\n" + "{" + str(self.ack) + "}"
                        self.s.sendto(send_message.encode(), i)

            self.client_list = {i:self.client_list[i]
                                for i in self.client_list
                                if self.client_list[i][2] == True}
                        


if __name__ == "__main__":
    test = server()
