import socket
import select
from time import sleep

SIZE = 1024


class Queue:
  def __init__(self):
    self.l = []

  def put(self,item):
    self.l.append(item)

  def get(self):
    try:
      item = self.l[0]
      del self.l[0]
      return item
    except IndexError:
      return None

  def empty(self):
    return len(self.l) == 0

class Server:
  def __init__(self,port=1148):
    self.port = port
    self.sock = socket.socket()
    self.sock.bind(('',self.port))
    self.sock.listen(3)
    self.clients = []
    self.infos = []
    self.q = Queue()

  def stop(self):
    for c in self.clients:
      c.close()
    self.sock.close()

  def accept_new_clients(self):
    new_conn = select.select([self.sock],[],[],0.05)[0]
    for c in new_conn:
      client,infos = c.accept()
      self.clients.append(client)
      self.infos.append(infos)

  def clear_dead_clients(self):
    i = 0
    while i < len(self.clients):
      if self.clients[i].fileno() == -1:
        del self.clients[i]
        del self.infos[i]
      else:
        i+=1

  def main_loop(self):
    self.accept_new_clients()
    self.clear_dead_clients()
    #print(f"I have {len(self.clients)} clients")
    for c in self.clients:
      if select.select([c],[],[],.05)[0]: # Is talking
        data = c.recv(SIZE)
        if data:
          self.q.put(data)
        else:
          c.close()


if __name__ == '__main__':
  s = Server()
  while True:
    s.main_loop()
    sleep(.1)
