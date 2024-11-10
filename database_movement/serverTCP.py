import socket
import AlphaBot
import threading
import time
import sqlite3

# Configurazione dell'indirizzo e della porta del server e buffer per i messaggi
MY_ADDRESS = ("0.0.0.0", 9090)
BUFFER_SIZE = 4096

# Connessione al database SQLite e caricamento dei movimenti predefiniti
conn = sqlite3.connect('MasoeroPollicino.db')
cur = conn.cursor()
cur.execute("SELECT * FROM MOVIMENTI")
database = cur.fetchall()

# Liste dei comandi e dei movimenti predefiniti
LISTA_COMANDI = ["w", "s", "a", "d", "release"]  # Comandi di base
LISTA_COMANDI_BASE = LISTA_COMANDI[:]
LISTA_MOVIMENTI_PREDEFINITI = []
LISTA_COMANDI_MOVIMENTI_PREDEFINITI = []

# Carica i movimenti predefiniti dal database e li aggiunge alle liste di comandi
for movimento_programmato in database:
    LISTA_COMANDI.append(movimento_programmato[0])
    LISTA_COMANDI_MOVIMENTI_PREDEFINITI.append(movimento_programmato[0])
    LISTA_MOVIMENTI_PREDEFINITI.append(movimento_programmato[1])

# Dizionario per tenere traccia dello stato dei comandi di base
dizionario_comandi = {elem: False for elem in LISTA_COMANDI_BASE if elem != "release"}
print(dizionario_comandi)
print(LISTA_COMANDI)
print(LISTA_COMANDI_BASE)
print(LISTA_MOVIMENTI_PREDEFINITI)
print(LISTA_COMANDI_MOVIMENTI_PREDEFINITI)

# Inizializzazione del robot "alice"
alice = AlphaBot.AlphaBot()
ultimo_ping = 0  # Variabile per tracciare l'ultimo segnale "ping" dal client

# Funzione per aggiornare lo stato dei comandi nel dizionario
def controllo_comandi(key, command):
    if key is None:
        dizionario_comandi[command] = True
    else:
        dizionario_comandi[key] = False
    return print(f"dizionario comandi: {dizionario_comandi}")

# Funzione per eseguire i comandi di base
def esegui_comandi_base():
    if dizionario_comandi["w"]:
        if dizionario_comandi["a"]:
            alice.setMotor(50, 100)  # Imposta i motori per andare avanti a sinistra
            print("Avanti-Sinistra")
            return ("Avanti-Sinistra")
        elif dizionario_comandi["d"]:
            alice.setMotor(100, 50)  # Avanti a destra
            print("Avanti-Destra")
            return ("Avanti-Destra")
        else:
            alice.forward()  # Avanti
            print("Avanti")
            return ("Avanti")
    elif dizionario_comandi["s"]:
        if dizionario_comandi["a"]:
            alice.setMotor(-50, -100)  # Indietro a sinistra
            print("Indietro-Sinistra")
            return ("Indietro-Sinistra")
        elif dizionario_comandi["d"]:
            alice.setMotor(-100, -50)  # Indietro a destra
            print("Indietro-Destra")
            return ("Indietro-Destra")
        else:
            alice.backward()  # Indietro
            print("Indietro")
            return ("Indietro")
    elif dizionario_comandi["a"]:
        alice.left()  # Sinistra
        print("Sinistra")
        return ("Sinistra")
    elif dizionario_comandi["d"]:
        alice.right()  # Destra
        print("Destra")
        return ("Destra")
    else:
        alice.stop()  # Stop se nessun comando è attivo
        print("stop")
        return ("stop")

# Funzione per eseguire un movimento temporizzato basato sui comandi ricevuti
def movimento_temporizzato(comando):
    com, tempo = comando.split('/')
    tempo = float(tempo)
    if com[0] == 'S':
        com = com[1:]
        m1, m2 = com.split('|')
        m1 = int(m1)
        m2 = int(m2)
        alice.setMotor(m1, m2)
        time.sleep(tempo)
    elif com == 'F':
        alice.forward()
        time.sleep(tempo)
    elif com == 'B':
        alice.backward()
        time.sleep(tempo)
    elif com == 'L':
        alice.left()
        time.sleep(tempo)
    elif com == 'R':
        alice.right()
        time.sleep(tempo)

# Funzione per eseguire una serie di movimenti predefiniti
def esegui_comandi_predefiniti(stringa):
    if ',' in stringa:
        comandi = stringa.split(',')
        for comando in comandi:
            movimento_temporizzato(comando)
        alice.stop()
    else:
        movimento_temporizzato(stringa)
        alice.stop()

# Funzione per controllare il segnale di comunicazione "ping" del client
def controlla_ping():
    global ultimo_ping
    while True:
        cont = ultimo_ping
        time.sleep(3)  # Attende 3 secondi tra i controlli
        if cont == ultimo_ping:
            alice.stop()
            print("Alice si ferma a causa della perdita della comunicazione con il client")
            break

# Funzione principale per la gestione del server
def main():
    key = None
    global ultimo_ping
    alice.stop()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    
    # Accetta una connessione in entrata
    connection, client_address = s.accept() 
    print(f"Il client {client_address} si è connesso")
    
    # Invia al client la lista dei comandi disponibili
    message = (f"Comandi disponibili: {LISTA_COMANDI}")
    connection.sendall(message.encode())

    # Avvia un thread per monitorare il "ping" dal client
    thread_ping = threading.Thread(target=controlla_ping, daemon=True)
    thread_ping.start()

    while True:
        # Riceve il comando dal client
        message = connection.recv(BUFFER_SIZE)
        comando = message.decode()
        print(f"comando ricevuto: {comando}")
        
        # Gestisce il "ping" per confermare la connessione attiva
        if comando == "ping":
            ultimo_ping += 1  # Aggiorna il timestamp dell'ultimo ping
            connection.sendall("heartbeat_ack".encode())  # Rispondi con ACK
            continue
        
        # Comando per terminare la comunicazione
        if comando == "esc":
            connection.sendall(f"comunicazione terminata".encode())
            break
        
        status = "error"
        
        # Controlla la struttura del comando
        if '|' in comando:
            key, comando = comando.split('|')
        
        # Esegue il comando se è nella lista dei comandi definiti
        if (comando in LISTA_COMANDI and comando != "release") or (comando == "release" and key in LISTA_COMANDI):
            status = "ok"
            if key is not None and key in LISTA_COMANDI_BASE:
                phrase = controllo_comandi(key, comando)
            else:
                phrase = controllo_comandi(None, comando)
            
            # Esegue i comandi base o predefiniti
            if comando in LISTA_COMANDI_BASE:
                esegui_comandi_base()
            else:
                num = LISTA_COMANDI_MOVIMENTI_PREDEFINITI.index(comando)
                esegui_comandi_predefiniti(LISTA_MOVIMENTI_PREDEFINITI[num])
        else:
            # Se il comando non è valido, invia un messaggio di errore
            if comando != "release":
                print(f"{comando} non in {LISTA_COMANDI}")
                phrase = f"{comando} non è presente in {LISTA_COMANDI}"
            else:
                print(f"{key} non in {LISTA_COMANDI}")
                phrase = f"{key} non è presente in {LISTA_COMANDI}"
        
        key = None
        
        # Invia lo stato e il messaggio di risposta al client
        connection.sendall(f"{status}|{phrase}".encode())
    
    # Ferma il robot e chiude la connessione
    alice.stop()
    connection.close()
    s.close()
    print("Comunicazione terminata")

# Avvia il server
if __name__ == "__main__":
    main()
