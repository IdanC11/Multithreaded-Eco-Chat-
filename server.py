"""
SERVER - CLIENT ECHO COMMUNICATION
BY IDAN CHERNETSKY

COMMANDS:
    > 'QUIT' - DISCONNECTS THE CLIENT FROM THE SERVER WITH THE CORRECT PASSWORD (12345)
    > 'TIME' - SENDS THE CLIENT THE CURRENT TIME AT THE SERVER
    > 'WHRU' - SENDS THE CLIENT THE SERVER'S NAME
    > 'MAC' - SENDS THE CLIENT THE SERVER'S MAC ADDRESS
    > 'CLIENTS NUM' - SENDS THE CLIENT THE NUMBER OF CLIENTS THAT ARE COMMUNICATING WITH THE SERVER
"""

from socket import *
from sys import *
from datetime import datetime
import threading
from tkinter import *
import subprocess
import uuid


PASSWORD = '12345'
HOST = 'localhost'
PORT = 50002
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 100
# responsible for the 'CLIENTS NUM' command
global CLIENTS_CONNECTED
CLIENTS_CONNECTED = 0

#responsible for the 'WHORU' command
def run_command(cmd):
    return subprocess.Popen(cmd,
                            shell=True, # not recommended, but does not open a window
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE).communicate()

#finds the first open port
def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

#establishes the connection with the client and gives him a new port
def create_new_connection(lock):
    global CLIENTS_CONNECTED
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(ADDR)
    sock.listen(MAX_CONNECTIONS)

    cont = True
    print("Waiting for connection")
    while cont:
        
        clientsock, addr = sock.accept()
        print(f"Connection from {addr}")
        #once the client connected > 1 more client is now communicating with the server
        CLIENTS_CONNECTED = CLIENTS_CONNECTED + 1
        
        #switches the connection to the new given port
        NEW_PORT = get_open_port()
        clientsock.send(str(NEW_PORT).encode('utf-8'))
        NEW_ADDR = (HOST, NEW_PORT)
        new_sock = socket(AF_INET, SOCK_STREAM)
        new_sock.bind(NEW_ADDR)
        new_sock.listen(1)
        #opens a thread for the communication between the server and the client
        threading.Thread(target=chat,args=(new_sock, lock)).start()
        print('thread started')
        clientsock.close()
        
    
    sock.close()

#the conversetion between the server and the client
def chat(sock, lock):
    global CLIENTS_CONNECTED
    
    BUFSIZ = 1024
    cont = True

    while cont:
        print(sock)
        clientsock, addr = sock.accept()
        while 1:
            check = True
            data = clientsock.recv(BUFSIZ)
            if not data:
                cont = False
                break
            
            if data[0:4].decode('utf-8') == 'QUIT':
                while 1:
                    msg = 'ENTER PASSWORD: '.encode('utf-8')
                    clientsock.send(msg)
                    data = clientsock.recv(BUFSIZ)
                    if not data:
                        cont = False
                        break
                    #responsible for disconnecting the connection between the server and the client after 
                        #getting the correct password
                    while data[0:5].decode('utf-8') != PASSWORD:
                        print(data[0:5].decode('utf-8'))
                        
                        
                        msg = 'WRONG PASSWORD, TRY AGAIN...'.encode('utf-8')
                        clientsock.send(msg)
                        data = clientsock.recv(BUFSIZ)
                        if not data:
                            cont = False
                            break
                    break
                cont = False
                check = False
                break
            
            #the 'TIME' command
            if data[0:4].decode('utf-8') == 'TIME':
                now = datetime.now()
                current_time = (now.strftime("%H:%M:%S")).encode('utf-8')
                print("Sending Time - ".encode('utf-8'), current_time)
                msg = "SERVER TIME = ".encode('utf-8') + current_time
                clientsock.send(msg)
                check = False
                
            #the 'WHORU' command
            if data[0:5].decode('utf-8') == 'WHORU':
                host_name = (run_command('hostname')[0]).strip().decode('utf-8')
                msg = host_name.encode('utf-8')
                clientsock.send(msg)
                check = False
                
            #the 'MAC' command
            if data[0:3].decode('utf-8') == 'MAC':
                mac_address = uuid.getnode()
                mac_address_str = ':'.join(format(s, '02x') for s in mac_address.to_bytes(6, byteorder='big'))
                msg = mac_address_str.encode('utf-8')
                clientsock.send(msg)
                check = False
                
            #the 'CLIENTS NUM' command
            if data[0:11].decode('utf-8') == 'CLIENTS NUM':
                msg = str(CLIENTS_CONNECTED).encode('utf-8')
                clientsock.send(msg)
                check = False
            
            #responsible for the echo massages
            if check:
                msg = data
                clientsock.send(msg)
        clientsock.close()
        
        #'lock' is making sure that no thread gets in the middle of the operation
        lock.acquire()
        CLIENTS_CONNECTED = CLIENTS_CONNECTED - 1
        lock.release()
        
    sock.close()

lock = threading.Lock()

#this thread is responsible for establishing a connection with each client
threading.Thread(target=create_new_connection, args=(lock,)).start()




