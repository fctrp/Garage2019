import socket

server_ip = "000.000.00.000"
port = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3.0)
s.bind((server_ip, port))
while True:
    try:
        data, addr = s.recvfrom(1024)
    except socket.timeout:
        print("timeout")
    else:
        print("data: {}, addr: {}".format(data, addr))