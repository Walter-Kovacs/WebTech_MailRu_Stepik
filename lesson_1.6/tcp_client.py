import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 1234))
while True:
    message = input("Input your message for server (type 'exit' for exit program):\n")
    if message.lower() == 'exit':
        break
    s.send(bytes(message, 'utf-8'))
    resp = s.recv(1024)
    print('\nServer response:\n', str(resp, 'utf-8'), '\n', sep='')
s.close()
