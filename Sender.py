import hashlib
import socket
import sys

PORT = 13000
BUF = 1024

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Can\'t create socket'
    sys.exit()

# Getting arguments
file_name = sys.argv[1]
host = sys.argv[2]

# Extracting file name from path, for sending to server
dirs = file_name.split('/')
s.sendto(dirs[len(dirs)-1], (host, PORT))

# Calculating hash for comparing with received file @ server
f = open(file_name, "rb")
data = f.read()
hash_obj = hashlib.md5(data)
hash_res = hashlib.md5(data).hexdigest()
print 'Hash: ' + hash_res
s.sendto(hash_res, (host, PORT))
f.close()

# Read file and send it to server
f = open(file_name, "rb")
while True:

    try:
        data = f.read(BUF)

        if not data:
            f.close()
            break

        s.sendto(data, (host, PORT))

    except socket.error, msg:
        print '\nError: ' + msg[1]
        sys.exit()

