from ast import Return
import socket
from _thread import *
import time

processSocket = socket.socket()
host = '127.0.0.1'
port = 1234
ThreadCount = 0
value_B = 0
old_value = 0
try:
    processSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('--------Process B--------')
print('Waiting for a Connection!')
processSocket.listen(5)

def abort(conn):
    conn.send(str.encode("ABORT"))
    print("ABORTED BY PROCESS B")

def put_value(val):
    value_B = val
    create_log(value_B)
    print("VALUE INSERTED")

def request_value():
    return value_B

def create_log(val):
    f = open("log_B.txt", "w")
    f.write("The inserted value is: " + str(val))
    f.close()

def execute(conn):
    while True:
        data = conn.recv(2048)
        temp = data.decode('utf-8')
        temp = str(temp)
        if temp == "PREPARE":
            conn.sendall(str.encode("ACK"))
            print("RECEIVED PREPARE, SENT ACK BACK TO COORDINATOR")
            # time.sleep(2)
            data = conn.recv(2048)
            temp = data.decode('utf-8')
            if temp == "COMMIT":
                print("RECEIVED COMMIT")
                print("COMMITTED")
            elif temp == 'ABORT':
                print("RECEIVED ABORT")
                print("ABORTED")
    
while True:
    Client, address = processSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(execute, (Client, ))
    ThreadCount += 1