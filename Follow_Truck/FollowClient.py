import socket
from time import sleep
host = '192.168.43.31'
port = 5560

def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def sendRecieve(s, ):
    message = "GET"
    s.send(str.encode(message))
    reply = s.recv(1024)
    print("we have recieved a reply")
    print("send closing message")
    s.send(str.encode("EXIT"))
    s.close()
    reply = reply.decode('utf-8')
    return reply

def Recieve():
    s = setupSocket()
    value = sendRecieve(s)
    return value
