#author: Sikder Huq
import socket
import os
import math
import json
 
# import thread module
from threading import Thread
import threading
from socketserver import ThreadingMixIn
 
print_lock = threading.Lock()

files = os.listdir('.')
files.remove('server.py')
print ('Found ' + str(len(files)) + ' files in the default directory')


        

class ClientThread(Thread):
 
    def __init__(self,conn, ip,port):
        Thread.__init__(self)
        self.conn = conn
        #self.conn.settimeout(5)
        self.ip = ip
        self.port = port
        print ("[+] New thread started for "+ip+":"+str(port))
 
 
    def run(self):
        while True:
            # data received from client
            data = self.conn.recv(1024)            
            if not data:
                print('Bye')
                break
            
            data =str(data.decode('iso-8859-1'))
            print_lock.acquire()
            print (data)
            print_lock.release()
     
            # if client is requesting for the list of iles, send the list 
            if data == 'send filelist': 
                print ('sending filelist')
                self.sendData (json.dumps(files))
                
            # if client is requesting for a particular file, send the file if available
            elif data.startswith ('send file '):
                fileName = data.split('send file ')[1]
                if fileName in files:
                    f = open(fileName, 'rb')
                    fileData = f.read()
                    f.close()
                    self.sendData (fileData.decode('iso-8859-1'))
                else:
                    self.sendData ('Error: file ' + str(filename) + 'not found')  
        #self.conn.close()
            
    def sendData(self, data):
        #send data to client in chunks
        for i in range(math.ceil(len(data)/1024)):
            toSend = data[i*1024 : min(1024*(i+1), len(data))]
            #print ('sending :' + toSend)
            self.conn.send(str.encode(toSend, 'iso-8859-1') )





 
 
 
threads = []   
 
 
if __name__ == '__main__':
    host = ""
 
    
    port = 3939
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    #s.settimeout(1)
    print("socket binded to post", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        (conn, (ip,port)) = s.accept()
        
        
        print('Connected to :', ip, ':', port)
        
 
        # Start a new thread and return its identifier
        newthread = ClientThread(conn, ip,port)
        newthread.start()
        threads.append(newthread)        
    s.close()
    
    for t in threads:
        t.join()    
