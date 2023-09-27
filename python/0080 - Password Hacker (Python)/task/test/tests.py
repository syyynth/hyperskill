from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from threading import Thread
from time import sleep
import socket
import random
import json

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


logins_list = [
    'admin', 'Admin', 'admin1', 'admin2', 'admin3',
    'user1', 'user2', 'root', 'default', 'new_user',
    'some_user', 'new_admin', 'administrator',
    'Administrator', 'superuser', 'super', 'su', 'alex',
    'suser', 'rootuser', 'adminadmin', 'useruser',
    'superadmin', 'username', 'username1'
]


def logins():
    for login in logins_list:
        yield login


def random_password():
    '''function - generating random password of length from 6 to 10'''
    return ''.join(random.choice(abc) for i in range(random.randint(6, 10)))


def random_login():
    return random.choice(list(logins()))


class TimeVulnerability(StageTest):

    def __init__(self, module):
        super().__init__(module)
        self.ready = False
        self.sock = None
        self.serv = None
        self.connected = False
        self.message = []
        self.password = None
        self.login = None

    def start_server(self):
        self.serv = Thread(target=lambda: self.server())
        self.serv.start()
        self.ready = False
        while not self.ready:
            try:
                sleep(0.1)  # socket needs to be set up before test
            except KeyboardInterrupt:
                pass

    def stop_server(self):
        self.sock.close()
        self.serv.join()

    def server(self):
        '''function - creating a server and answering clients'''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 9090))
        self.ready = True
        try:
            self.sock.listen(1)
            conn, addr = self.sock.accept()
            conn.settimeout(16)
            while True:
                data = conn.recv(1024)
                self.message.append(data.decode('utf8'))
                self.connected = True
                if len(self.message) > 100_000_000:
                    conn.send(json.dumps({'result': 'Too many attempts to connect!'}).encode('utf8'))
                    break
                if not data:
                    break

                try:
                    login_ = json.loads(data.decode('utf8'))['login']
                    password_ = json.loads(data.decode('utf8'))['password']
                except:
                    conn.send(json.dumps({'result': 'Bad request!'}).encode('utf8'))
                    continue

                if login_ == self.login:
                    if self.password == password_:
                        conn.send(json.dumps({'result': 'Connection success!'}).encode('utf8'))
                        break
                    elif self.password.startswith(password_):
                        sleep(0.1)
                        conn.send(json.dumps({'result': 'Wrong password!'}).encode('utf8'))
                    else:
                        conn.send(json.dumps({'result': 'Wrong password!'}).encode('utf8'))
                else:
                    conn.send(json.dumps({'result': 'Wrong login!'}).encode('utf8'))
            conn.close()
        except:
            pass

    def generate(self):
        self.message = []
        self.password = random_password()
        self.login = random_login()
        self.start_server()
        return [
            TestCase(args=['localhost', '9090'],
                     attach=[self.password, self.login])
        ]

    def check(self, reply, attach):
        self.stop_server()

        if not self.connected:
            return CheckResult.wrong("You didn't connect to the server")

        real_password, real_login = attach
        try:
            json_reply = json.loads(reply)
        except:
            return CheckResult.wrong(
                'The output of your program is not a valid JSON:\n' + reply
            )
        try:
            password = json_reply['password']
        except KeyError:
            return CheckResult.wrong(
                'The output of your program did not contain the field "password":\n' + reply
            )
        except TypeError:
            return CheckResult.wrong(
                'The output of your program did not contain the field "password":\n' + reply
            )
        try:
            login = json_reply['login']
        except KeyError:
            return CheckResult.wrong(
                'The output of your program did not contain the field "login":\n' + reply
            )
        except TypeError:
            return CheckResult.wrong(
                'The output of your program did not contain the field "login":\n' + reply
            )
        if login != real_login:
            return CheckResult.wrong('The login you printed is not correct')
        elif password != real_password:
            return CheckResult.wrong('The password you printed is not correct')
        find_first_letter = False
        for i in self.message:
            log = json.loads(i)['login']
            pas = json.loads(i)['password']
            if find_first_letter is False and len(pas) == 1 and log == real_login and real_password.startswith(pas):
                find_first_letter = True
            if find_first_letter is True:
                if log != real_login:
                    return CheckResult.wrong('You should find a correct login and then use only it')
                if pas[0] != real_password[0]:
                    return CheckResult.wrong(
                        'When you find a first letter you should then start your passwords with it')
            if len(pas) > 1:
                if pas[0:-1] != real_password[0:len(pas[0:-1]) - 1]:
                    return CheckResult.wrong(
                        'You have already found the first %d letters of the password. Use them as a beginning' % len(
                            pas[0:-1]))
            return CheckResult.correct()


if __name__ == '__main__':
    test = TimeVulnerability('hacking.hack')
    test.run_tests()
    test.stop_server()
