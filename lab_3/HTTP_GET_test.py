# Import socket library
from socket import *
from time import *

# Host and port
host = 'www.google.com'
port = 80

# Declare socket
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(1.0)  


# Connect to the host
try:
    clientSocket.connect((host, port))
    print ("Successfully connected to port " + str(port))
except:
    print (host + " cannot be connected to port " + str(port))



# Send GET request
try:   	 
    z = clientSocket.send(str.encode("GET / HTTP/1.0\r\nHost: " + host + "\r\nConnection: close\r\n\r\n"))
    print ("successfully sent " + str(z) + " bytes to port " + str(port))
except:
    print ("Cannot send data to port " + str(port))

   	 
# Listen and store the response
response = ''   	 
while True:           	 
    received = clientSocket.recv(4096)
    response+= received.decode('iso-8859-1')           	 
    if len(received) == 0:
        break
   	 
# Print the response
print (response)
   	 
# discard the header and store only the content
content =  response.split('\r\n\r\n')[1]

clientSocket.close()




