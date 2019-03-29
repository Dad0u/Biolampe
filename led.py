from time import sleep
import machine
from neopixel import NeoPixel


#MAX = 255
MAX = 10
#RGBW
NPIX = 64
FULL = (MAX,)*4
WHITE = (0,0,0,MAX)
BLACK = (0,)*4
RED = (MAX,0,0,0)
GREEN = (0,MAX,0,0)
BLUE = (0,0,MAX,0)


pix = NeoPixel(machine.Pin(14),NPIX,bpp=4)


def scroll(delay=.02):
  for i in range(NPIX):
    pix[i] = BLACK
    i = (i+1)%NPIX
    pix[i] = WHITE
    sleep(delay)
    pix.write()


def blink(color=WHITE,delay=.5):
  for i in range(2):
    pix.fill(color)
    pix.write()
    sleep(delay)
    pix.fill(BLACK)
    pix.write()
    sleep(delay)


def static(color=WHITE,delay=1):
  pix.fill(color)
  pix.write()
  sleep(delay)


def pulse(color=WHITE,delay=.01,npoint=50):
  r,g,b,w = color
  npoint = 50
  for i in range(npoint):
    pix.fill([int(i*k/npoint) for k in color])
    pix.write()
    sleep(delay)
  for i in range(npoint):
    pix.fill([int((npoint-i)/npoint*k) for k in color])
    pix.write()
    sleep(delay)


def center4(color=WHITE):
  pix.fill(BLACK)
  for p in [27,28,35,36]:
    pix[p] = color
  pix.write()

def tiny_blink(color=WHITE,blink_color=BLACK,delay=.5):
  pix.fill(color)
  pix.write()
  sleep(delay)
  for i in [0,1,8,9]:
    pix[i] = blink_color
  pix.write()
  sleep(delay)

def off():
  static(BLACK)

actions = {
    b'1': scroll,
    b'2': blink,
    b'3': static,
    b'4': pulse,
    b'5': center4,
    b'6': off
    }
