# IMPORTS
import socket

# CREATE SOCKET
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ASK FOR PORT FROM USER
PORT = int(input("Enter the PORT for the server: "))

# CONNECT TO THE SERVER
clientsocket.connect(("10.1.21.46", PORT))

# SEND FLAG TO SERVER
clientsocket.send("CLIENT".encode())

# GET CURRENT LIST FROM SERVER
response = clientsocket.recv(1024).decode()
print(response)

# SEND i, j TO SERVER
i = int(input("Enter i: "))
j = int(input("Enter j: "))
clientsocket.send((str(i)+" "+str(j)).encode())

# CLOSE THE CONNECTION
clientsocket.close()