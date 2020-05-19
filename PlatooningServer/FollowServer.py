# Raspberry Pi tutorial 27 Socket Communication 1
import socket
#from LeadServer import getStoredValue
host = ''
port = 5560

storedValue = "8"

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("socket bind complete.")
    return s


def setupConnection(s):
    s.listen(1)  # allows 1 connection at a time
    conn, address = s.accept()
    print("connected to: " + address[0] + ":" + str(address[1]))
    return conn


def GET():
    global storedValue
    reply = storedValue
    print("replying with " + str(reply))
    return reply


def REPEAT ( dataMessage):
    reply = dataMessage[1]
    return reply

def CONFIRM ( dataMessage):
    reply = dataMessage[0]
    return reply


def dataTransfer(conn):
    # a big loop that sends and recieves data
    global storedValue
    x=0
    while x <=1:  # loop twice
        data = conn.recv(1024)
        data = data.decode('utf-8')
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'GET':
            value = GET()
            reply = str(storedValue)
            print("getting" + str(storedValue))
            x=x+2
        elif command == 'REPEAT':
            reply = REPEAT(dataMessage)
            print("repeating")
        elif command == '0' or '1' or '2' or '3' or '4' or '5' or '6' or'7' or '8' or'8' or '10':
            print(str(command))
            storedValue = str(command)
            reply = "chk"
            x=x+2
        elif command == 'EXIT':
            print(" client has disconnected ")
            x=x+1
            break
        elif command == 'KILL':
            print("Server is shutting down")
            break
        else:
            print("unknown command")
            reply = 'Unknown Command'
        # send the reply back to the client
        conn.sendall(str.encode(reply))
        #print("Data has been sent!")
    conn.close()


while True:
    s = setupServer()

    while True:
        try:
            conn = setupConnection(s)
            dataTransfer(conn)

        except:
            print("exception on while loop")
            conn.close()
            s.close()
            break
