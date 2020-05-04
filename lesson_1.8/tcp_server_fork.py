import os
import socket

FILE_BORDER = '-' * 100 + '\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 8080))
s.listen(10)
os.fork()  # two client

while True:
    conn, addr = s.accept()
    hello_string = "Hello, client! I'm server. Type file name you want to get, 'close' - for close connection."
    conn.sendall(hello_string.encode('utf-8'))
    while True:
        conn.sendall('\n:'.encode('utf-8'))
        file_name = conn.recv(512).decode('utf-8').rstrip('\r\n')
        if file_name == 'close':
            conn.sendall('Closing connection...\n'.encode('utf-8'))
            break

        file_path = os.path.join(os.getcwd(), file_name)
        try:
            with open(file_path, 'r') as file:
                response = FILE_BORDER + file.read() + FILE_BORDER
                conn.sendall(response.encode('utf-8'))
        except FileNotFoundError:
            response = 'File Not Found!\nUse one of:\n'
            for elem in os.scandir():
                if elem.is_file():
                    response += elem.name + '\n'
            conn.sendall(response.encode('utf-8'))
        except:
            response = 'Server error'
            conn.sendall(response.encode('utf-8'))
    conn.close()
