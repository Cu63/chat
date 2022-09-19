import socket


class Client():
    def __init__(self, ip='0.0.0.0', port=9998):
        self.ip = ip
        self.port = port
        self.connection = None

    def creat_connection(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))
        msg = self.connection.recv(1024).decode('utf8')
        if msg == 'Enter your name: ':
            s = input(msg)
            self.connection.send(s.encode('utf8'))
        else:
            print('[!?] Something wrong>...')
            self.connection.close()


def main():
    connection = Client()
    connection.creat_connection()


if __name__ == '__main__':
    main()
