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

def color(i,w=0):
  i = min(max(i,0),1)
  if i < 1/3:
    i = int(i*3*MAX)
    j = MAX-i
    return (j,i,0,w)
  elif i < 2/3:
    i = int((i-1/3)*3*MAX)
    j = MAX-i
    return (0,j,i,w)
  else:
    i = int((i-2/3)*3*MAX)
    j = MAX-i
    return (i,0,j,w)

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

def rainbow(w=0):
  for i in range(8):
    for j in range(8):
      pix[8*i+j] = color(i/8,w)
  pix.write()

def color_sweep(npoint=255,delay=.05,w=0):
  for i in range(npoint):
    pix.fill(color(i/npoint))
    pix.write()
    sleep(delay)

def moving_dot4(color=WHITE,delay=.1):
  for i in range(7):
    for j in range(7):
      if i % 2 == 0: j = 6-j
      pix.fill(BLACK)
      for k in [0,1,8,9]:
        pix[8*i+j+k] = color
      pix.write()
      sleep(delay)

def interp(x,y,color):
  x = min(max(0,x),7)
  y = min(max(0,y),7)
  xa = int(x)
  dx = x-xa
  xb = xa+1
  ya = int(y)
  dy = y-ya
  yb = ya+1
  pix[xa*8+ya] = [int((1-dx)*(1-dy)*i) for i in color]
  pix[xa*8+yb] = [int((1-dx)*dy*i) for i in color]
  pix[xb*8+ya] = [int(dx*(1-dy)*i) for i in color]
  pix[xb*8+yb] = [int(dx*dy*i) for i in color]
  pix.write()


x,y = 0,0
speedx = .15896
speedy = .135478
c = 0
def bounce(delay=.01):
  global x,y,c,speedx,speedy
  x += speedx
  y += speedy
  c += .0025
  if c>1:
    c-=1
  if x > 7:
    x = 14-x
    speedx = -speedx
  elif x < 0:
    x = -x
    speedx = -speedx
  if y > 7:
    y = 14-y
    speedy = -speedy
  elif y < 0:
    y = -y
    speedy = -speedy
  pix.fill(BLACK)
  interp(x,y,color(c))
  sleep(delay)


actions = {
    b'1': scroll,
    b'2': blink,
    b'3': static,
    b'4': pulse,
    b'5': center4,
    b'6': off
    }
