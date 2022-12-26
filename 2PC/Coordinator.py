from _thread import *
import socket
import time

ProcessSocket_1 = socket.socket()
ProcessSocket_2 = socket.socket()
host_1 = '127.0.0.1' #Process A
port_1 = 1233 
host_2 = '127.0.0.1' #Process B
port_2 = 1234

systemSocket = socket.socket()
host = '127.0.0.1'
port = 1235
thread_num = 0
try:
    systemSocket.bind((host, port))
except socket.error as e:
    print("ERROR: ",str(e))

try:
    ProcessSocket_1.connect((host_1, port_1))
    ProcessSocket_2.connect((host_2, port_2))
except socket.error as e:
    print(str(e))

print('TRANSACTION COORDINATOR IS RUNNING')

def put_value(pid, value):
    match pid:
        case 1:
            start_time = time.time()
            ProcessSocket_1.send(str.encode(str(value)))
            resp_1 = ProcessSocket_1.recv(1024)
            if (resp_1.decode('utf-8')) == "ACK" and time.time() - start_time < 10:
                print("SUCCESS")
            else:
                ProcessSocket_1.sendall(str.encode('ABORT'))
                ProcessSocket_1.sendall(str.encode('ROLLBACK'))
                print("PROCESS ABORTED BY COORDINATOR AND ROLLBACK IS SENT")
        case 2:
            start_time = time.time()
            ProcessSocket_2.send(str.encode(str(value)))
            resp_2 = ProcessSocket_2.recv(1024)
            if (resp_2.decode('utf-8')) == "ACK" and time.time() - start_time < 10:
                print("SUCCESS")
            else:
                ProcessSocket_2.sendall(str.encode('ABORT'))
                ProcessSocket_2.sendall(str.encode('ROLLBACK'))
                print("PROCESS ABORTED BY COORDINATOR AND ROLLBACK IS SENT")

def request_value():
    ProcessSocket_1.sendall(str.encode('GET'))
    print("GET SENT")

def create_log_abort():
    f = open("log_Coordinator.txt", "w")
    f.write("THE COORDINATOR HAS ABORTED")
    f.close()

def create_log_commit():
    f = open("log_Coordinator.txt", "w")
    f.write("THE COORDINATOR HAS COMMITED")
    f.close()

def two_phase_commit():
    send_prepare()
    print("SENT PREPARE")
    if wait_for_all_acks():
        send_commit()
        print("COMMIT SENT")
    else:
        ProcessSocket_1.sendall(str.encode('ABORT'))
        ProcessSocket_2.sendall(str.encode('ABORT'))
        print("ABORT SENT")
        print("PROCESS ABORTED BY COORDINATOR")
    

def send_prepare():
    ProcessSocket_1.sendall(str.encode('PREPARE'))
    ProcessSocket_2.sendall(str.encode('PREPARE'))

def wait_for_all_acks():
    ack_1 = ProcessSocket_1.recv(2048)
    ack_2 = ProcessSocket_2.recv(2048)
    if ack_1.decode('utf-8') == "ACK" and ack_2.decode('utf-8') == "ACK":
        print("ACKNOWLEDGEMENT RECEIVED")
        return True
    else:
        return False

def send_commit():
    ProcessSocket_1.sendall(str.encode('COMMIT'))
    ProcessSocket_2.sendall(str.encode('COMMIT'))
    print("COMMIT SENT")

def main():
    while True:
        # process = int(input("Enter the process:"))
        value = int(input("Enter the value:"))
        two_phase_commit()
        #put_value(process,value)

if __name__ == "__main__":
    main()