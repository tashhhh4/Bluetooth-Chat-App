import socket

# Finding the bluetooth adapter's MAC address in Linux:
# bluetoothctl
# > list
MY_BLUETOOTH_ADAPTER_MAC_ADDRESS = 'd0:39:57:9d:5f:78'

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.bind((MY_BLUETOOTH_ADAPTER_MAC_ADDRESS, 4))
server.listen(1)

client, addr = server.accept()

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        print(f'Message: {data.decode("utf-8")}')
        message = input('Enter message: ')
        client.send(message.encode('utf-8'))
except OSError as e:
    pass

client.close()
server.close()