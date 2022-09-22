import socket
import threading


class Server():
    def __init__(self, ip='0.0.0.0', port=9998):
        self.ip = ip
        self.port = port
        self.server = None # socket of the server
        self.users = dict() # dict of users
        self.msg_queue = [] # save msg from all users

    def run(self):
        # open socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.thread = ServerThread(self.users, self.msg_queue)
        self.thread.start()
        print(f'[*] Starting server on {self.ip}:{self.port}')

    def listen(self):
        # listen socke for new connection
        while True:
            user = {'sock': 0, 'thread': 0, 'login': ''}
            self.server.listen(5)
            client, address = self.server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            client.send('[*] Enter your name: '.encode('utf8'))
            login = client.recv(1024).decode('utf8')
            client.send(('[*] Hello, %s' % login).encode('utf-8'))
            # add user to the users dict
            user['sock'] = client
            user['login'] = login
            # start thread for user
            user['thread'] = ClientThread(client, login, self.msg_queue)
            user['thread'].start()
            self.users[address] = user

    def shut_down(self):
        print('[*] Shut down the server...')
        print(self.msg_queue)
        # close connection for all active users
        self.thread.disconnect()
        for addr in self.users:
            self.users[addr]['thread'].disconnect()


class ServerThread(threading.Thread):
    def __init__(self, users, msg_queue):
        threading.Thread.__init__(self)
        self.users = users
        self.msg_queue = msg_queue
        self.isactive = True

    def run(self):
        print('[*] Start ServerThread')
        while self.isactive:
            self.chek_users()
            self.send_msg()

    def chek_users(self):
        for addr in self.users.copy():
            if self.users[addr]['thread'].get_status() == False:
                print(f'[*] Detelet {addr[0]}:{addr[1]} from user list')
                self.users.pop[addr]

    def send_msg(self):
        while self.msg_queue != [] and self.isactive:
            s = self.msg_queue.pop(0)
            for addr in self.users.copy():
                login = self.users[addr]['login']
                if s[:s.find(': ')] != login:
                    self.users[addr]['sock'].send(s.encode('utf-8'))

    def disconnect(self):
        self.isactive = False

class ClientThread(threading.Thread):
    def __init__(self, clientSock, login, chat):
        threading.Thread.__init__(self)
        self.sock = clientSock
        self.login = login
        self.chat = chat
        self.isactive = True
        print('[*] New user added: %s' % self.login)

# start user thread
    def run(self):
        print('[*] Start listen stream from %s' % self.login)
        # listen msg from user
        msg = ''
        while self.isactive:
            msg = self.sock.recv(1024).decode('utf8')
            print('[*] Recive data form user: %s' % self.login)
            if msg != 'bye':
                # add to msg_queue
                self.chat.append('%s: %s' % (self.login, msg))
            else:
                self.disconnect()
                break

# close connection
    def disconnect(self):
        print('[*] Close connection for %s' % self.login)
        self.sock.send('[*] Connection closed'.encode('utf-8'))
        self.isactive = False

    def get_status(self):
        return self.isactive


def main():
    try:
        server = Server()
        server.run()
        server.listen()
    except KeyboardInterrupt:
        server.shut_down()


if __name__ == '__main__':
    main()
