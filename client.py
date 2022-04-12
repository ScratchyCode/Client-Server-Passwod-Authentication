import socket
import hashlib

host = input("Remote host: ")
port = int(input("Port: "))

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
response = client.recv(2048)

# input username
user = input(response.decode())	
client.send(str.encode(user))
response = client.recv(2048)

# input password
password = input(response.decode())
password = hashlib.sha256(str.encode(password)).hexdigest()
client.send(str.encode(password)) # send only hashed passwd over network

#response: status of connection
#1: registeration successful
#2: connection successful
#3: login failed

# receive response 
response = client.recv(2048)
response = response.decode()
print(response)

client.close()
