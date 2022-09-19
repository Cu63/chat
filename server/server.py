import socket
#import threading


class Server():
    def __init__(self, ip='0.0.0.0', port=9998):
        self.ip = ip
        self.port = port
        self.server = None
        self.users = []

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        print(f'[*] Starting server on {self.ip}:{self.port}')

    def listen(self):
        self.server.listen(5)
        client, address = self.server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client.send('Enter your name: '.encode('utf8'))
        login = client.recv(1024).decode('utf8')
        self.users = ClientThread(client, address, login)

    def shut_down(self):
        pass


class ClientThread(threading.Thread):
    def __init__(self, clientAddr, clientSock, login):
        threading.Thread.__init__(self)
        self.sock = clientSock
        self.addr = clientAddr
        self.login = login
        print('[*]New user added: %s', self.login)

    def run(self):
        msg = ''
        while msg != 'bye':
            msg = self.sock.recv(1024).decode('utf8')
            print('[*] Recive data form user: %s' % self.login)
            print('%s: %s' % (self.login, msg))
        print('Client at ', self.addr, ' disconected...')


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
