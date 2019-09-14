import socket

server_ip = "000.000.000.0"
port = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'Hello UDP', (server_ip, port))
