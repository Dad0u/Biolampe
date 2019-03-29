import network

n = network.WLAN(network.STA_IF)
n.active(True)
n.connect('Dadou-Phone','mylittlepony')
print("Connected!" if n.isconnected() else 'Failed to connect')

isconnected = n.isconnected
