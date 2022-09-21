import socket
import threading


class Server():
    def __init__(self, ip='0.0.0.0', port=9998):
        self.ip = ip
        self.port = port
        self.server = None
        self.users = dict() 
        self.msg_queue = []

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        print(f'[*] Starting server on {self.ip}:{self.port}')

    def listen(self):
        while True:
            self.server.listen(5)
            client, address = self.server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            client.send('[*] Enter your name: '.encode('utf8'))
            login = client.recv(1024).decode('utf8')
            client.send(('[*] Hello, %s' % login).encode('utf-8'))
            self.users[address] = ClientThread(client, address,
                                               login, self.msg_queue)
            self.users[address].start()

    def shut_down(self):
        print('[*] Shut down the server...')
        print(self.msg_queue)
        for addr in self.users:
            self.users[addr].disconnect()


class ClientThread(threading.Thread):
    def __init__(self, clientSock, clientAddr, login, chat):
        threading.Thread.__init__(self)
        self.sock = clientSock
        self.addr = clientAddr
        self.login = login
        self.chat = chat
        self.isactive = True
        print('[*] New user added: %s' % self.login)

    def run(self):
        print('[*] Start listen stream from %s' % self.login)
        msg = ''
        while self.isactive:
            msg = self.sock.recv(1024).decode('utf8')
            print('[*] Recive data form user: %s' % self.login)
            if msg != 'bye':
                self.chat.append('%s: %s' % (self.login, msg))
            else:
                break
        print('Client at ', self.addr, ' disconected...')

    def disconnect(self):
        print('[*] Close connection for %s' % self.login)
        self.isactive = False


def main():
    try:
        server = Server()
        server.run()
        server.listen()
    except KeyboardInterrupt:
        server.shut_down()


if __name__ == '__main__':
    main()
