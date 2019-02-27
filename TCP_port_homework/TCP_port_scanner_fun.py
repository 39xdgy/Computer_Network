from socket import *
for i in range(101):
    try:
        c = socket(AF_INET, SOCK_STREAM)
        c.settimeout(.5)
        if not c.connect_ex(("www.cornellcollege.edu", i)): print("Port "+ str(i) + " success.")
        c.close()
    except: continue
