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
        print(f'[*] Starting server on {self.ip}:{self.port}')

    def listen(self):
        # listen socke for new connection
        while True:
            user = {'sock': 0, 'thread': 0}
            self.server.listen(5)
            client, address = self.server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            client.send('[*] Enter your name: '.encode('utf8'))
            login = client.recv(1024).decode('utf8')
            client.send(('[*] Hello, %s' % login).encode('utf-8'))
            # add user to the users dict
            user['sock'] = client

            # start thread for user
            user['thread'] = ClientThread(client, address,
                                               login, self.msg_queue)
            user['thread'].start()
            self.users[address] = user

    def shut_down(self):
        print('[*] Shut down the server...')
        print(self.msg_queue)
        # close connection for all active users
        for addr in self.users:
            self.users[addr]['thread'].disconnect()


class ServerThread(threading.Thread):
    def __init__(self, users, msg_queue):
        threading.Thread.__init__(start)
        self.users = users
        self.msg_queue = msg_queue
        self.isactive = True

    def run(self):
        print('[*] Start ServerThread')
        while self.isactive:
            self.chek_users()
            self.send_msg()

    def chek_users(self):
        for addr in self.users:
            if users[addr].get_status() == False:
                print(f'[*] Detelet {addr[0]}:{addr[1]} from user list')
                users.pop[addr]

    def send_msg(self):
        for addr in users:
            pass


class ClientThread(threading.Thread):
    def __init__(self, clientSock, clientAddr, login, chat):
        threading.Thread.__init__(self)
        self.sock = clientSock
        self.addr = clientAddr
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
        print('Client at ', self.addr, ' disconected...')

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
