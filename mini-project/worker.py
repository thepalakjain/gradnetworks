from itertools import product
from string import ascii_lowercase
import socket
import hashlib
import sys

def crack_password(hashval,fix):

    if len(hashval) != 32:
        print('hash value shorter than expected!')
        return
    if len(fix) > 4:
        print('fixed string longer than expected!')
        return

    hashval = hashval.lower()
    unfixed = 5 - len(fix)

    endings = [''.join(i) for i in list(product(ascii_lowercase,repeat=unfixed))]
    passwords = [fix + e for e in endings]

    for p in passwords:
        if hashlib.md5(p.encode()).hexdigest() == hashval:
            return p

    return "no-password-found"

HOST = socket.gethostname()
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:

    instructions = s.recv(1024).decode("utf-8")

    if instructions:
        hashval,fix = instructions.split()
        print("\njob received!\n")
        #print("checking passwords beginning with " + fix + " for hash value " + hashval + "...")

        result = crack_password(hashval,fix)
        # if result != "no-password-found":
        #     print("password found!\n ~~~~" + result + "~~~~")
        # else:
        #     print(result)

        response = hashval + ' ' + result
        s.sendall(response.encode())
        print("sent response")
        #print(response)

