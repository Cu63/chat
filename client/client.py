import socket
import threading


class Client():
    def __init__(self, ip='0.0.0.0', port=9998):
        self.ip = ip
        self.port = port
        self.login = ''
        self.connection = None
        self.thread = None

    def creat_connection(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))
        print('[*]Connectin to the chat...')
        msg = self.connection.recv(1024).decode('utf8')
        if msg == '[*] Enter your name: ':
            self.login = input(msg)
            self.connection.send(self.login.encode('utf8'))
            self.thread = GetMsg(self.connection)
            self.thread.start()
        else:
            print('[!?] Something wrong>...')
            self.connection.close()
        print('[*] Connected')

    def get_name(self):
        return self.login

    def send_msg(self, s):
        try:
            self.connection.send(s.encode('utf-8'))
        except:
            print("[!?] Can't send message...")

    def close(self):
        print('[*] Disconnect')
        self.thread.stop()
        self.connection.close()


class GetMsg(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.isactive = True

    def run(self):
        print('[*] Loading chat...')
        while self.isactive == True:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                print(msg)
            except:
                print("[!?] can't receive msg from server")
                self.sock.close()

    def stop(self):
        self.isactive = False


def main():
    connection = Client()
    connection.creat_connection()
    msg = ''
    while msg != 'bye':
        msg = input("%s: " % connection.get_name())
        connection.send_msg(msg)

    connection.close()


if __name__ == '__main__':
    main()
