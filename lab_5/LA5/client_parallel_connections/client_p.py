import socket
import json
import time
file_list = []

def recv_message(s):
    data_recv = ''
    while True:
        data = s.recv(1024)
        data_recv += str(data.decode('iso-8859-1'))

        if not data or len(data) < 1024:
            break

    return data_recv

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 3939
    s_list = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))

    data_recv = ''

    s.send(str.encode('send filelist', 'iso-8859-1'))

    data_recv = recv_message(s)

    file_list = json.loads(data_recv)
    #print(file_list)
    #print(str(len(file_list)) + ' files available')
    #print(type(file_list))

    read_length = len(file_list)//5
    file_index = 0
    for i in range(5):
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ss.connect((host, port))

        s_list.append(ss)


    before = time.time()

    
    while file_index != len(file_list):
        for i in range(len(s_list)):
            now_s = s_list[i]

            now_s.send(str.encode('send file ' + str(file_list[file_index]), 'iso-8859-1'))

            data_recv = recv_message(now_s)

            f = open(file_list[file_index], 'wb')
            f.write(str.encode(data_recv, 'iso-8859-1'))
            f.close()
            file_index += 1
            if(file_index == len(file_list)):
                break

    for s in s_list:
        s.close()



            
            
        
    now = time.time()
    print("It takes", now - before, "seconds. ")
