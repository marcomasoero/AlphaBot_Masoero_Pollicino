import socket
import AlphaBot
import threading
import time

MY_ADDRESS = ("0.0.0.0", 9090)
BUFFER_SIZE = 4096
LISTA_COMANDI = ["w", "s", "a", "d", "release"]
dizionario_comandi = {elem: False for elem in LISTA_COMANDI if elem != "release"}
print(dizionario_comandi)
alice = AlphaBot.AlphaBot()

ultimo_ping = 0

def controllo_comandi(key, command):
    if key == None:
        dizionario_comandi[command] = True
    else:
        dizionario_comandi[key] = False
    return print(f"dizionario comandi: {dizionario_comandi}")

def esegui_comandi():
    if dizionario_comandi["w"]:
        if dizionario_comandi["a"]:
            alice.setMotor(50, 100)
            print("Avanti-Sinistra")
            return ("Avanti-Sinistra")
        elif dizionario_comandi["d"]:
            alice.setMotor(100, 50)
            print("Avanti-Destra")
            return ("Avanti-Destra")
        else:
            alice.forward()
            print("Avanti")
            return ("Avanti")
    elif dizionario_comandi["s"]:
        if dizionario_comandi["a"]:
            alice.setMotor(-50, -100)
            print("Indietro-Sinistra")
            return ("Indietro-Sinistra")
        elif dizionario_comandi["d"]:
            alice.setMotor(-100, -50)
            print("Indietro-Destra")
            return ("Indietro-Destra")
        else:
            alice.backward()
            print("Indietro")
            return ("Indietro")
    elif dizionario_comandi["a"]:
        alice.left()
        print("Sinistra")
        return ("Sinistra")
    elif dizionario_comandi["d"]:
        alice.right()
        print("Destra")
        return ("Destra")
    else:
        alice.stop()
        print("stop")
        return ("stop")

def controlla_ping():
    global ultimo_ping
    while True:
        cont = ultimo_ping
        time.sleep(3)
        if cont == ultimo_ping:
            alice.stop()
            print("Alice si ferma a causa della perdità della comunicazione con il client")
            break

def main():
    key = None
    global ultimo_ping
    alice.stop()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    connection, client_address = s.accept() #bloccante
    print(f"Il client {client_address} si è connesso")
    message = (f"Comandi disponibili: {LISTA_COMANDI}")
    connection.sendall(message.encode())

    thread_ping = threading.Thread(target=controlla_ping, daemon=True)
    thread_ping.start()

    while True:
        message = connection.recv(BUFFER_SIZE) #bloccante
        comando = message.decode()
        print(f"comando ricevuto: {comando}")
        if comando == "ping":
            ultimo_ping += 1  # Aggiorna l'ultima ricezione del heartbeat
            connection.sendall("heartbeat_ack".encode())  # Rispondi con ACK
            continue
        if comando == "esc":
            connection.sendall(f"comunicazione terminata".encode())
            break
        status = "error"
        if '|' in comando:
            key, comando = comando.split('|')
        if (comando in LISTA_COMANDI and comando != "release") or (comando == "release" and key in LISTA_COMANDI):
            status = "ok"
            if key != None:
                phrase = controllo_comandi(key, comando)
            else:
                phrase = controllo_comandi(None, comando)
            esegui_comandi()
        else:
            if comando != "release":
                print(f"{comando} non in {LISTA_COMANDI}")
                phrase = f"{comando} non è presente in {LISTA_COMANDI}"
            else:
                print(f"{key} non in {LISTA_COMANDI}")
                phrase = f"{key} non è presente in {LISTA_COMANDI}"
        key = None
        
        connection.sendall(f"{status}|{phrase}".encode())
    alice.stop()
    connection.close()
    s.close()
    print("Comunicazione terminata")

if __name__ == "__main__":
    main()