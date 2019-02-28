import socket


IP_addr = '127.0.0.1'
Port = 62

Buffer_size = 1024

client_list = {}

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('', Port))

while 1:
    message, client_tuple = s.recvfrom(Buffer_size)

    message = message.decode("utf-8")

    if not client_tuple in client_list:
        client_list[client_tuple] = message
        print(message)
        for i in client_list:
            intro = message + " is joined into the chat Room. "
            s.sendto(intro.encode(), i)

    else:
        nick_name = client_list[client_tuple]
        for i in client_list:
            send_message = nick_name + ": " + message
            s.sendto(send_message.encode(), i)
