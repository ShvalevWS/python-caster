from pyrtcm import RTCMReader
import serial
import socket
import base64


class Tools:
    def __init__(self):
        self.stream = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.rtr = RTCMReader(self.stream)


    def get_line(self):
        for (raw_data, parsed_data) in self.rtr:
            if '<RTCM(1005' in str(parsed_data):
                print(f'Got 1005 RTCM string  -  {parsed_data}')
                return True
            else:
                print('Searching')
                continue


    def print_parsed(self):
        for (raw_data, parsed_data) in self.rtr:
            print(parsed_data)


    def print_GNGGA(self):
        while True:
            line = str(self.stream.readline())
            result = line.replace('b', '').replace("'", "")
            dict_line = result.split(",")
            word = "$GNGGA"
            if dict_line[0] == word:
                final = ",".join(dict_line)
                print(final)


    def make_line(self):
        count = 0
        lst = []
        for (raw_data, parsed_data) in self.rtr:
            RTCM = ['<RTCM(4072', '<RTCM(1077', '<RTCM(1097', '<RTCM(1127', '<RTCM(1230', '<RTCM(1005']
            if count < 15 or str(parsed_data) in RTCM:
                lst.append(raw_data)
                count += 1
            else:
                print('List collected. Formatting now!')
                break
        #string = b''.join(lst)
        return lst



class Caster:
    def __init__(self):
        self.username = 'Visystem1'
        self.password = 'stem21'
        self.mount = '/U-BLOX'


    def parse_headers(self, request):
        heads = []
        auth = ''
        method = ''
        reqst_text = request.split('\r\n')
        for elms in reqst_text:
            heads.append(elms)
            for i in heads:
                if 'Authorization:' in i:
                    auth = i.split(':')[1][7:]
                elif 'GET' in i:
                    method = i.split()
        return auth, method[1], method[0]


    def authentication(self, auth):
        username = self.username
        password = self.password
        true_auth = base64.b64encode(f'{username}:{password}'.encode('ascii'))
        true_auth = true_auth.decode('ascii')
        if auth == true_auth:
            print('Authentication passed!')
            return True
        else:
            print(f'Wrong credentials. The auth was - {auth}')
            return False


    def mountpt_check(self, mount):
        if mount == self.mount:
            print('Right mountpoint')
            return True
        else:
            print('Wrong mountpoint')
            return False


    def method_check(self, method):
        if method == 'GET':
            print('Right method')
            return True
        else:
            print('Wrong method')
            return False


    def castering(self, host, port):
        tools = Tools()
        cast = Caster()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        print(f'Starting a caster on {host}:{port}')
        while True:
            client_connection, client_address = sock.accept()

            request = client_connection.recv(1024).decode()
            print(request)

            if cast.authentication(auth=cast.parse_headers(request=request)[0]) == True \
                    and cast.mountpt_check(mount=cast.parse_headers(request=request)[1]) == True \
                    and cast.method_check(method=cast.parse_headers(request=request)[2]):
                try:
                    response = tools.make_line()
                    client_connection.sendall(response)
                    print(f"We're sent - {response}")
                except Exception as e:
                    print(e)
            elif '$GNGGA' in request:
                pass
            else:
                response = b'Sorry, your request method/creds/mountpoint is wrong. Bye-bye!'
                client_connection.sendall(response)
                client_connection.close()
