import socket

for i in range(0, 101):
    try:
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect.settimeout(.5)
        
        if not connect.connect_ex(("www.cornellcollege.edu", i)):
            print("Port "+ str(i) + " success. ")
        else:
            print("Port closed " + str(i))
        connect.close()
        
    except:
        print("Something is wrong.")
