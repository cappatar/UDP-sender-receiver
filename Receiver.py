import hashlib
import socket
import sys

HOST = ''
PORT = 13000
BUF = 1024

file_closed = True

while file_closed:
    print 'Waiting for incoming data...'

    try:
        UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error, msg:
        print 'Error - Can\'t create socket: ' + msg[1]
        sys.exit()

    try:
        UDPSock.bind((HOST, PORT))
    except socket.error, msg:
        print 'Error - Bind failed: ' + msg[1]
        sys .exit()

    data, address = UDPSock.recvfrom(BUF)
    file_name = data.strip()
    data, address = UDPSock.recvfrom(BUF)
    hash_from_sender = data.strip()

    while True:

        try:
            aFile = open(file_name, 'a+b')
            file_closed = False
            UDPSock.settimeout(3)
            data, address = UDPSock.recvfrom(BUF)

            if not data:
                aFile.close()
                file_closed = True
                break

            aFile.write(data)
            reply = 'File downloaded.'
            UDPSock.sendto(reply, address)

        # If time out, break inner loop, create new socket
        except socket.timeout, msg:
            buff = aFile.read()

            # Calculating hash for comparing received file with original
            hash_obj = hashlib.md5(buff)
            hash_res = hashlib.md5(buff).hexdigest()
            aFile.close()
            file_closed = True
            print 'Hash: ' + hash_res
            print 'Hash from Sender: ' + hash_from_sender
            if hash_res == hash_from_sender:
                print 'same hash'
            else:
                print 'different hash'
            UDPSock.close()
            break