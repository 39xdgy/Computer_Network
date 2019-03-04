# author: Sikder Huq
import socket
import json
import time
fileList = []


def receiveMessage(s):
    dataReceived = ''
    #receive data from server in chunks
    while True:
        #print('receiving data...')
        data = s.recv(1024)
        #print('Received: ' + str(data.decode('iso-8859-1')))
        dataReceived += str(data.decode('iso-8859-1'))
    
        
        if not data or len(data) < 1024:
            break
        
    return dataReceived
                
    
 
if __name__ == '__main__':
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
 
    # Define the port on which you want to connect
    port = 3939
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
 
    # connect to server on local computer
    s.connect((host,port))   
    
    dataReceived = ''
    
 
    # send request for filelist to server        
    s.send(str.encode ('send filelist', 'iso-8859-1'))   
    
    #receive response
    dataReceived = receiveMessage(s)      

    # print the received message
    #print('Received from the server :'+ dataReceived)
    
    # extract filenames from the message received
    fileList = json.loads(dataReceived)
    print (str(len(fileList)) + ' files available')
    before = time.time()
    #download files
    for i in range(len(fileList)):
        fileName = fileList[i]
        
        # send file download request to server
        s.send(str.encode ('send file ' + str(fileName) , 'iso-8859-1'))
        
        #receive response
        dataReceived = receiveMessage(s) 
        
        #write data on file
        f = open(fileName, 'wb')
        f.write(str.encode(dataReceived, 'iso-8859-1'))
        f.close()
        
        
        
    # close the connection
    s.close()

    now = time.time()

    print("It takes", now-before, "seconds. ")
