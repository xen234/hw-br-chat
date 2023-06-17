import socket
from threading import Thread

try:
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 50010
    separator_token = "<SEP>"

    client_sockets = set()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    def listen(cs):
        while True:
            try:
                msg = cs.recv(1024).decode()
            except Exception as e:
                client_sockets.remove(cs)
            else:
                msg = msg.replace(separator_token, ": ")
            for client_socket in client_sockets:
                client_socket.send(msg.encode())

    while True:
        client_socket, client_address = s.accept()
        client_sockets.add(client_socket)
        t = Thread(target=listen, args=(client_socket,))
        t.daemon = True
        t.start()

except Exception as e:
    print('Error!!!')

finally:
    
    for cs in client_sockets:
        cs.close()
    s.close()
