import socket
from pynput import keyboard
import threading
import time

SERVER_ADDRESS = ("localhost", 9090)
BUFFER_SIZE = 4096
INTERVALLO_PING = 1

# Dizionario per tracciare lo stato dei tasti (True se premuto, False se rilasciato)
pressed_keys = {}

def manda_ping(socket):
    while True:
        print("ping")
        socket.sendall("ping".encode())
        ack = socket.recv(BUFFER_SIZE)
        if ack.decode() != "heartbeat_ack":
            print("Heartbeat ACK non ricevuto!")
        time.sleep(INTERVALLO_PING)

def on_press(socket, key):
    try:
        if key not in pressed_keys or not pressed_keys[key]:
            # Se il tasto non è già premuto, invia la pressione
            pressed_keys[key] = True
            print(f'alphanumeric key {key.char} pressed')
            socket.sendall(f"{key.char}".encode())
            messaggio = socket.recv(BUFFER_SIZE)
            print(messaggio.decode())
    except AttributeError:
        # Tasti speciali (ad esempio shift, ctrl, etc.)
        if key not in pressed_keys or not pressed_keys[key]:
            pressed_keys[key] = True
            print(f'special key {key} pressed')

def on_release(socket, key):
    if key == keyboard.Key.esc:
        # Se il tasto è ESC, interrompi il listener
        socket.sendall("esc".encode())
        messaggio = socket.recv(BUFFER_SIZE)
        print(messaggio.decode())
        return False
    
    if key in pressed_keys and pressed_keys[key]:
        # Quando il tasto viene rilasciato, invia il messaggio di rilascio
        pressed_keys[key] = False
        print(f'{key.char} released')
        socket.sendall(f"{key.char}|release".encode())
        messaggio = socket.recv(BUFFER_SIZE)
        print(messaggio.decode())
 
    

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    messaggio = s.recv(BUFFER_SIZE)
    print(messaggio.decode())
    
    # Avvia thread per inviare heartbeat
    heartbeat_thread = threading.Thread(target=manda_ping, args=(s,), daemon=True)
    heartbeat_thread.start()

    with keyboard.Listener(
        on_press=lambda key: on_press(s, key),
        on_release=lambda key: on_release(s, key)) as listener:
        listener.join()

if __name__ == "__main__":
    main()