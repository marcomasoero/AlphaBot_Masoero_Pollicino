import socket
from pynput import keyboard  # Libreria per monitorare la pressione dei tasti
import threading
import time

# Impostazioni di connessione
SERVER_ADDRESS = ("192.168.1.134", 9090)
BUFFER_SIZE = 4096
INTERVALLO_PING = 1  # Intervallo in secondi tra un ping e l'altro

# Dizionario per tracciare lo stato dei tasti: True se premuto, False se rilasciato
pressed_keys = {}

# Funzione per inviare periodicamente un "ping" al server per mantenere attiva la connessione
def manda_ping(socket):
    while True:
        print("ping")  # Debug per monitorare l'invio del ping
        socket.sendall("ping".encode())  # Invia "ping" al server
        ack = socket.recv(BUFFER_SIZE)  # Attende una risposta dal server
        if ack.decode() != "heartbeat_ack":  # Se il server non risponde correttamente
            print("Heartbeat ACK non ricevuto!")  # Notifica il mancato riconoscimento del ping
        time.sleep(INTERVALLO_PING)  # Attende prima del prossimo ping

# Funzione chiamata alla pressione di un tasto
def on_press(socket, key):
    try:
        # Verifica se il tasto è già stato premuto (per evitare ripetizioni)
        if key not in pressed_keys or not pressed_keys[key]:
            pressed_keys[key] = True  # Segna il tasto come premuto nel dizionario
            print(f'alphanumeric key {key.char} pressed')  # Debug per indicare la pressione
            socket.sendall(f"{key.char}".encode())  # Invia il carattere del tasto al server
            messaggio = socket.recv(BUFFER_SIZE)  # Riceve e stampa la risposta del server
            print(messaggio.decode())
    except AttributeError:
        # Caso in cui viene premuto un tasto speciale (ad esempio shift, ctrl)
        if key not in pressed_keys or not pressed_keys[key]:
            pressed_keys[key] = True  # Segna il tasto speciale come premuto
            print(f'special key {key} pressed')

# Funzione chiamata al rilascio di un tasto
def on_release(socket, key):
    if key == keyboard.Key.esc:
        # Se il tasto ESC viene rilasciato, invia "esc" per terminare la connessione
        socket.sendall("esc".encode())  # Invia il messaggio di uscita al server
        messaggio = socket.recv(BUFFER_SIZE)
        print(messaggio.decode())  # Stampa la risposta del server
        return False  # Termina il listener per l'input da tastiera
    
    # Se il tasto è rilasciato e presente nel dizionario, aggiorna lo stato
    if key in pressed_keys and pressed_keys[key]:
        pressed_keys[key] = False  # Aggiorna lo stato del tasto
        print(f'{key.char} released')  # Debug per indicare il rilascio
        socket.sendall(f"{key.char}|release".encode())  # Invia al server il rilascio del tasto
        messaggio = socket.recv(BUFFER_SIZE)
        print(messaggio.decode())  # Stampa la risposta del server
 
# Funzione principale che gestisce la connessione e il listener dei tasti
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP/IP
    s.connect(SERVER_ADDRESS)  # Connette il client al server
    messaggio = s.recv(BUFFER_SIZE)  # Riceve e stampa il messaggio di benvenuto del server
    print(messaggio.decode())
    
    # Avvia un thread per l'invio del "ping" periodico
    heartbeat_thread = threading.Thread(target=manda_ping, args=(s,), daemon=True)
    heartbeat_thread.start()

    # Configura il listener per catturare la pressione e il rilascio dei tasti
    with keyboard.Listener(
        on_press=lambda key: on_press(s, key),  # Gestisce la pressione del tasto
        on_release=lambda key: on_release(s, key)  # Gestisce il rilascio del tasto
    ) as listener:
        listener.join()  # Mantiene attivo il listener fino alla chiusura

# Avvia l'applicazione client
if __name__ == "__main__":
    main()
