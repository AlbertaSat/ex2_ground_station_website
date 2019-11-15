import socket

def send(data):
    """Transmit data to the sat sim socket
    Params:
        @data (str) : message string with format '<command> <arg1> <arg2> ...'
    Return:
        @resp (str) : response from sat sim
    """
    HOST = '127.0.0.1'
    PORT = 65432

    data = bytes(data, 'utf-8')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(data)
        resp = s.recv(2048).decode('utf-8')
        return resp
