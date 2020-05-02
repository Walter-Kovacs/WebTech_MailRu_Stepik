import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 1234))
s.listen(10)  # clients queue length

server_running = True
while server_running:
    conn, addr = s.accept()
    print('accept connection')
    print(conn)
    while True:
        print('accepting data...')
        data = conn.recv(1024)
        if not data:
            break

        data_str = str(data, 'utf-8')
        print('input data as utf-8 string:', data_str)
        if data_str == "close":
            break
        if data_str == "stop":
            server_running = False
            conn.send(b"stopping server by request...")
            break

        t = time.localtime()
        t = f"{t.tm_hour}:{t.tm_min}:{t.tm_sec} {t.tm_mday}.{t.tm_mon}.{t.tm_year}"
        data += b"\nNow time: " + bytes(str(t), 'utf-8')
        conn.send(data)
    print('close connection')
    conn.close()

print('server stopped')
