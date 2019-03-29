import net # Connect to the network
from server_led import Server
import led

action = led.static
s = Server()
while True:
  while not net.isconnected():
    led.tiny_blink(blink_color=led.RED)
    if net.isconnected():
      for i in range(4):
        led.tiny_blink(blink_color=led.GREEN,delay=.2)
      action = led.static
  s.main_loop()
  while not s.q.empty():
    data = s.q.get().strip()
    if data in led.actions:
      action = led.actions[data]
  action()
