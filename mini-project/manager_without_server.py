import socket
import threading
import time
import sys
from string import ascii_lowercase

hashlist = ['c5385419ca7f0dc26e3cbc32aa651f68', 'ce2c5237eb3c586ecc014ebeaea1b067', 'c561147bce4d7350fcd2b353630c3ba8', 'e1faa44ba7d5f136d6a7e9d4f4503776', '04ca0fd390b5378d6c1e3b2590d18652', '4301d0bb854b5957a78b8e26886f2ab7', '38b35906a313b39a4360c09eb5346944', 'f27b6e23e686afd0c2200dc945910a88', '93ef47dfb75349b28682744063b90067', '1231da4e10d810661e1d6318408ad64d', '4c500bbacdfe7bd574ba987f424f9f3e', '6112d03da193a10c9d609b8411ba865d', '58fad276ca2847dca6166ac978f20705', 'b72bd06017c9d939bf93806b008b4522', '51774fb8ab8bd8f424a551ac9fb2c1a1']
final_output = []
final_times = []

# declares the address and the port defining the socket for the inital connection
HOST = socket.gethostname()
WORKER_PORT = 50000 

#global variable
workers = []
worker_sockets = {}
worker_status = {}
passwords_cracked = {}
job_start_time = {}
job_list = []
time_list = []
workername = 1
threshold = 1000

def connect_to_workers():
    while True:
        # connect to a worker
        w_sock, _ = s_worker.accept()
        global workername
        w = workername
        workername += 1
        workers.append(w)
        worker_status[w] = "idle"
        worker_sockets[w] = w_sock

        # start a new thread
        new_thread = threading.Thread(target = get_response,args = (w,))
        new_thread.setDaemon(True)
        new_thread.start()
        print("\nconnected to a new worker, thread started for worker " + str(w) + "...\n")

def get_response(w):
    while True:        
        if worker_status[w] != "idle":
            #print("waiting for worker response")
            response_time = time.time() - job_start_time[w]
            if response_time > threshold:
                job_list.append(worker_status[w])
                worker_status.pop(w)
                job_start_time.pop(w)
                workers.remove(w)
                w_sock = worker_sockets.pop(w)
                w_sock.close()
                print("worker " + str(w) + " down...")
                return

            w_sock = worker_sockets[w]
            response = w_sock.recv(1024).decode("utf-8")
        
            if response:
                print(response)
                hashval,password = response.split()
                if password == "no-password-found":
                    worker_status[w] = "idle"
                else:
                    passwords_cracked[hashval] = password
                    print("password " + password + " for hashval " + hashval + " found by worker " + str(w) + "!!")
                    worker_status[w] = "idle"

def assign_jobs():
    while True:
        while len(job_list) != 0:
            #print("jobs left: " + str(len(job_list)))
            #print("assigning more jobs!")
            for w in workers:
                #print(str(worker_status))
                if worker_status[w] == "idle" and len(job_list)>0:
                    print("assigning to " + str(w))
                    instructions = job_list.pop()
                    w_sock = worker_sockets[w]
                    w_sock.sendall(instructions.encode())
                    job_start_time[w] = time.time()
                    worker_status[w] = instructions


def handle_request(hashval):

    if len(hashval) != 32:
        print("invalid hash value!")

    #start timer
    start_time = time.time()

    #add hashval to passwords_cracked
    passwords_cracked[hashval] = "no-password-found"

    #create jobs
    for a in ascii_lowercase:
        for b in ascii_lowercase:
            if passwords_cracked[hashval] == "no-password-found":
                job_list.append(hashval + " " + a + b)

    #wait for cracked value
    while True:
        #if password is found
        if passwords_cracked[hashval] != "no-password-found":
            #note stop time
            stop_time = time.time()
            time_list.append((start_time,stop_time))
            #remove any pending jobs for this hashval
            for index,job in enumerate(job_list):
                h,_ = job.split()
                if h == hashval:
                    job_list.pop(index)
            #output the password and remove from list
            password = passwords_cracked.pop(hashval)
            print("password found!")
            print("hashval: " + hashval)
            print("password: " + password)
            print("time_list: " + str(time_list))
            response = password + " " + str(start_time) + " " + str(stop_time)
            final_output.append(hashval + " " + response)
            final_times.append(stop_time-start_time)
            return
            

if __name__ == '__main__':

    #create worker socket
    s_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_worker.bind((HOST, WORKER_PORT))
    s_worker.listen(10)
    print("\nworker socket has been initialized. listening for connections...\n")
    print(HOST+ ":" + str(WORKER_PORT))

    num_workers = int(input("how many workers?"))

    # spawn thread to connect to workers
    worker_thread = threading.Thread(target = connect_to_workers)
    worker_thread.setDaemon(True)
    worker_thread.start()

    #spawn thread for assigning jobs to workers
    job_thread = threading.Thread(target = assign_jobs)
    job_thread.setDaemon(True)
    job_thread.start()

    while True:
        if len(workers) == num_workers:
            for hashval in hashlist:   
                handle_request(hashval)
            break

    print(final_output)
    for t in final_times:
        print t



        
        
