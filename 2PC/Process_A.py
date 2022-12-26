import socket
from _thread import *
import time
import random 

processSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
value_A = 0
old_value = 0
try:
    processSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('--------Process A--------')
print('Waiting for a Connection!')
processSocket.listen(5)

def abort(conn):
    conn.send(str.encode("ABORT"))
    print("ABORTED BY PROCESS A")

def put_value(val):
    value_A = val
    create_log(value_A)
    print("VALUE INSERTED")

def request_value():
    return value_A

def create_log(val):
    f = open("log_A.txt", "w")
    f.write("The inserted value is: " + str(val))
    f.close()

def introduce_failure(conn):
    print("Process A is down")
    conn.sendall(str.encode("NO"))
    data = conn.recv(2048)
    temp = data.decode('utf-8')
    if temp == "COMMIT":
        print("COMMITTED")
    elif temp == 'ABORT':
        abort(conn)

def execute(conn):
    # m = "PREPARE"
    while True:
        # start_time = time.time()
        data = conn.recv(2048)
        temp = data.decode('utf-8')
        temp = str(temp)
        r = random.randint(1,3)
        if(r == 1):
            print("Process A is down")
            conn.sendall(str.encode("NO"))
            time.sleep(3)
            data = conn.recv(2048)
            temp = data.decode('utf-8')
            if temp == "COMMIT":
                print("RECEIVED COMMIT")
                print("COMMITTED")
            elif temp == 'ABORT':
                print("RECEIVED ABORT")
                print("ABORTED")
        if(r == 2):
            time.sleep(3)
            print("TIMED OUT: DID NOT RECEIVE PREPARE FROM COORDINATOR")
            conn.sendall(str.encode("NO"))
            data = conn.recv(2048)
            temp = data.decode('utf-8')
            if temp == "COMMIT":
                print("RECEIVED COMMIT")
                print("COMMITTED")
            elif temp == 'ABORT':
                print("RECEIVED ABORT")
                print("ABORTED")
        else:
            if temp == "PREPARE":
                conn.sendall(str.encode("ACK"))
                print("RECEIVED PREPARE, SENT ACK BACK TO COORDINATOR")
                data = conn.recv(2048)
                temp = data.decode('utf-8')
                if temp == "COMMIT":
                    print("COMMITTED")
                elif temp == 'ABORT':
                    abort(conn)


while True:
    Client, address = processSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(execute, (Client, ))
    ThreadCount += 1