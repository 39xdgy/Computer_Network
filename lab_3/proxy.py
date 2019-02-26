import socket
import select
import time
import sys

TCP_IP = '127.0.0.1'
TCP_Port = 80
Buffer_Size = 1024
get_http_format_0 = "GET / HTTP/1.0\r\nHost: "
get_http_format_1 = "\r\nConnection: close\r\n\r\n"

class Proxy_server:

    def __init__(self):
        self.cache = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_Port))
        s.listen(1)
        conn, addr = s.accept()
        print('Connection address:', addr)
        while(True):
            try:
                data = conn.recv(Buffer_size)
                print("Get Data From %s" %data)
                data_tuple = (data, 80)
                self.main_logic(data_tuple)
            except:
                print("No data")
                
    def main_logic(self, data_tuple):

        while(True):
            if self.check_cache(data_tuple):
                print(self.get_cache(data_tuple))
            else:
                html_data = self.get_HTML(data_tuple)
                self.add_cache(html_data, data_tuple, time.time())
        
    def get_HTML(self, data_tuple):

        host, port = input_tuple

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.settimeout(1.0)

        try:
            clientSocket.connect((host, port))
            print("Successfully connected to the port.")
        except:
            print(host + " cannot be connected to port" + str(port))
        
        http_get_request = get_http_format_0 + host + get_http_format_1
        print(http_get_request)

        try:
            z = clientSocket.send(str.encode(http_get_request))
            print("successfully sent" + str(z) + "bytes to port" + str(port))
        except:
            print("Cannot send data to port " + str(port))

        
        result = ''
        while(True):
            received = clientSocket.recv(4096)
            result += received.decode('iso-8859-1')
            if(len(received) == 0):
                break

        result = result.split('\r\n\r\n')[1]
        
        return result

    def add_cache(self, html, data_tuple, intro_time):
        self.cache[data_tuple] = (html, intro_time)

    def check_cache(self, data_tuple):
        return data_tuple in self.cache

    def update_cache(self, html, data_tuple, intro_time):
        temp = {data_tuple: (html, intro_time)}
        self.cache.update(temp)

    def get_cache(self, data_tuple):
        return self.cache[data_tuple]


    
        

if __name__ == "__main__":
    test = Proxy_server()
    
