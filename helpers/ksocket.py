import socket

class KSocketClient:

  def __init__(self, sock=None):
    if sock is None:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
      self.sock = sock

  def kconnect(self, host, port):
    self.sock.connect((host, port))

  def ksend(self, data):
    self.sock.send(data)

  def kreceive(self):
    chunks = []
    while True:
      chunk = self.sock.recv(2048)
      if not chunk:
        break
      else:
        chunks.append(chunk)
    return b''.join(chunks)
