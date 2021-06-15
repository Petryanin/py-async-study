import socket
import selectors

selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    selector.register(fileobj=server_socket,
                      events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print('[ACCEPT_CONNECTION] Connection from', addr)
    selector.register(fileobj=client_socket,
                      events=selectors.EVENT_READ, data=send_message)
    print(f'[ACCEPT_CONNECTION] Client {addr} registered')


def send_message(client_socket):
    request = client_socket.recv(4096)

    if request:
        print(f'[SEND_MESSAGE] Sending response...')
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        print(f'[SEND_MESSAGE] Client unregistered')
        client_socket.close()


def event_loop():
    while True:
        print('[EVENT_LOOP] Start of the WHILE True loop...')
        events = selector.select()  # Main block
        print('[EVENT_LOOP] Start of the FOR loop...')
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)

        print('[EVENT_LOOP] End of all loops...\n')


if __name__ == '__main__':
    server()
    event_loop()
