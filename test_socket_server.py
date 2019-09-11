import socket

server_ip = "000.000.00.000"
port = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((server_ip, port))
while True:
    data, addr = s.recvfrom(1024)
    print("data: {}, addr: {}".format(data, addr))
