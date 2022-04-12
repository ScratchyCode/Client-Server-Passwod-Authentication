import socket
import os
import threading
import hashlib

# create socket (TCP) connection
serverSocket = socket.socket(family = socket.AF_INET,type = socket.SOCK_STREAM) 
#host = "127.0.0.1"
host = ""
port = int(input("Listening port: "))
threadCount = 0

try:
    serverSocket.bind((host,port))
except socket.error as errore:
    print(str(errore))

print("Waiting for a connection...")
serverSocket.listen(5)
HashTable = {}

# Function for each client 
def threaded_client(connection):
    connection.send(str.encode("Enter username: ")) # request username
    name = connection.recv(2048)
    connection.send(str.encode("Enter password: ")) # request password
    password = connection.recv(2048)
    password = password.decode()
    name = name.decode()
    
# REGISTERATION PHASE
    # if new user, regiter in hashtable dictionary
    if name not in HashTable:
        HashTable[name]=password
        connection.send(str.encode("Registeration successful")) 
        print("Registered: ",name)
        print("{:<8} {:<20}".format("USER","PASSWORD"))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
    
    else:
        # if already existing user, check if the entered password is correct
        if(HashTable[name] == password):
            connection.send(str.encode("Connection successful")) # response code for connected client
            print("Connected : ",name)
        else:
            connection.send(str.encode("Login failed")) # response code for login failed
            print("Connection denied: ",name)
    while True:
        break
    connection.close()

##############
#    main    #
##############
while True:
    client,address = serverSocket.accept()
    client_handler = threading.Thread(target=threaded_client,args=(client, ))
    client_handler.start()
    threadCount += 1
    print("Connection request: " + str(threadCount))

serverSocket.close()
