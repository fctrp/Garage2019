import socket

server_ip = "000.000.00.000"
port = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'Hello UDP', (server_ip, port))
