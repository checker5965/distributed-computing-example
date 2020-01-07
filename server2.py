# IMPORTS
import socket
import time
import threading
from ast import literal_eval

# SETTING THINGS UP
IP = "10.1.21.46"
PORT = 8001

# IP TO PRIORITIZE
SPECIAL_IP = "10.1.20.115"

# LIST OF SERVERS
servers = [(IP, 8000), (IP, 8002)]

# ORIGINAL LIST
L = [x for x in range(10)]

# CREATE SOCKET
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((IP, PORT))

# BECOME SERVER
serversocket.listen(128)
print("Server is running! (IP address - %s, Port - %s)" % (IP, PORT))

# REQUEST POOL
requestPool = []

# CONSENSUS THREAD
def commitRequests():
    
    global requestPool
    print("Consensus: Asking for requests.")

    # CREATE TEMPORARY POOL
    tempPool = []
    
    # CONNECT TO EVERY SERVER AND RECEIVE REQUESTS
    for server in servers:
        consensussocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        consensussocket.connect(server)
        consensussocket.send("SERVER".encode())
        
        # RECEIVE REQUESTS TILL YOU GET OVER FLAG
        while True:
            response = consensussocket.recv(1024).decode()
            if response == "OVER":
                break
            tempPool.append(literal_eval(response))
        
        # CLOSING CONNECTION
        consensussocket.close()

    # BUSY WAIT TO PRESERVE REQUEST POOL 
    print("Consensus: Waiting.")
    time.sleep(5)
    
    # ADD NEW REQUESTS TO REQUEST POOL
    requestPool = requestPool + tempPool

    # SORT BASED ON TIMESTAMP
    requestPool.sort(key=lambda x: x[0])
    
    # COMMIT REQUESTS FROM SPECIAL IP
    for request in requestPool:
        if request[1][0] == SPECIAL_IP:
            L[request[2]], L[request[3]] = L[request[3]], L[request[2]]

    # COMMIT REQUESTS FROM THE REMAINING IPs
    for request in requestPool:
        if request[1][0] == SPECIAL_IP:
            continue
        L[request[2]], L[request[3]] = L[request[3]], L[request[2]]

    # EMPTY REQUEST POOL
    requestPool = []
    print("CONSENSUS COMPLETE!")

    # WAIT TO START NEXT CONSENSUS THREAD
    threading.Timer(60, commitRequests).start() 
    

# CLIENT THREAD
def checkingThread(clientsocket, address):

    # ACCEPT FLAG
    flag = clientsocket.recv(1024).decode()

    # IF CLIENT, SEND LIST AND ACCEPT i, j
    if flag == "CLIENT":
        print("Connected to client.")
        clientsocket.send(str(L).encode())
        response = clientsocket.recv(1024).decode().split(" ")
        ctime = time.time()
        i, j = int(response[0]), int(response[1])
        requestPool.append([ctime, address, i, j])
        clientsocket.close()
    
    # IF SERVER, SEND ALL REQUESTS FROM REQUEST POOL
    elif flag == "SERVER":
        print("Consensus: Sending Requests.")
        for element in requestPool:
            clientsocket.send(str(element).encode())
            print("Sent Request")
        clientsocket.send("OVER".encode())
        clientsocket.close()

    return

# START CONSENSUS THREAD
threading.Timer(60, commitRequests).start()

while True:

    # ACCEPT CONNECTIONS
    (clientsocket, address) = serversocket.accept()
    print("Got a connection from ", address)

    # CREATE A THREAD AND START IT
    t1 = threading.Thread(target = checkingThread, args = (clientsocket, address, ))
    t1.start()