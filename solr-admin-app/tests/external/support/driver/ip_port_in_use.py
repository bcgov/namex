import socket


class IpPortInUse(object):

    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def is_in_use(self):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        timeout = socket.timeout
        socket.timeout = 1
        try:
            my_socket.connect((self.ip_address, self.port))
            return True
        except socket.error:
            return False
        finally:
            my_socket.close()
            socket.timeout = timeout