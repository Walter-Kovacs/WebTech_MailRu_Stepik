import os
import select
import socket

RESPONSE_CLOSE_CONNECTION_BY_REQUEST = "Connection closing by request...".encode('utf-8')
RESPONSE_HELLO = "Hello, client! Type file name you want to get, 'close' - for close connection.\n:".encode('utf-8')
RESPONSE_FILE_NOT_FOUND = "File not found! Try one of this:\n".encode('utf-8')
SENDING_FILE_BORDER = '-' * 100 + '\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 8080))
s.settimeout(0)
s.listen(10)

connections_list = []
connections_hello = {}

while True:
    # TODO: wrap in functions, or make class and methods
    try:
        conn, addr = s.accept()
    except BlockingIOError:
        pass
    else:
        connections_list.append(conn)
        print('Accepted connection:', conn, sep='\n')
        print('Connections count:', len(connections_list))
    readable, writeable, err = select.select(connections_list, connections_list, [], 0)
    for w_conn in writeable:
        if w_conn not in connections_hello:
            print("Sending 'hello' to client", w_conn.getpeername())
            w_conn.sendall(RESPONSE_HELLO)
            connections_hello[w_conn] = True

    for r_conn in readable:
        print('Reading from', r_conn.getpeername(), '...')
        request = r_conn.recv(1024).decode('utf-8').rstrip('\r\n')  # TODO: OSError if client is out without 'close'
        print('\tRequest:', request)
        if r_conn in writeable:
            if request != 'close':
                file_path = os.path.join(os.getcwd(), request)
                print("\tTrying to get file:", file_path)
                if os.path.isfile(file_path):
                    print("\tSending file...")
                    with open(file_path, 'r') as file:
                        response = SENDING_FILE_BORDER + file.read() + SENDING_FILE_BORDER
                        response = response.encode('utf-8')
                else:
                    print("\tFile not found. Sending 'file not found' response...")
                    response = RESPONSE_FILE_NOT_FOUND
                    for elem in os.scandir():
                        if elem.is_file():
                            response += str(elem.name + '\n').encode('utf-8')
                response += ":".encode('utf-8')
                r_conn.sendall(response)
                print("\tDone")
            else:
                print("\tClosing connection by request...")
                r_conn.sendall(RESPONSE_CLOSE_CONNECTION_BY_REQUEST)
                r_conn.close()
                connections_list.remove(r_conn)
                del connections_hello[r_conn]
