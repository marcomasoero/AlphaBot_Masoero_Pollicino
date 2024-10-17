import socket
import AlphaBot
import threading
import time

MY_ADDRESS = ("0.0.0.0", 9090)
BUFFER_SIZE = 4096
LISTA_COMANDI = ["w", "s", "a", "d", "release"]
dizionario_comandi = {elem: False for elem in LISTA_COMANDI if elem != "release"}
alice = AlphaBot.AlphaBot()
key = None
ultimo_ping = 0

def controllo_comandi(key, command):
    if key == None:
        dizionario_comandi[command] = True
    else:
        dizionario_comandi[command] = False

def esegui_comandi():
    if dizionario_comandi["w"]:
        if dizionario_comandi["a"]:
            alice.setMotor(50, 100)
            return ("Avanti-Sinistra")
        elif dizionario_comandi["d"]:
            alice.setMotor(100, 50)
            return ("Avanti-Destra")
        else:
            alice.forward()
            return ("Avanti")
    elif dizionario_comandi["s"]:
        if dizionario_comandi["a"]:
            alice.setMotor(-50, -100)
            return ("Indietro-Sinistra")
        elif dizionario_comandi["d"]:
            alice.setMotor(-100, -50)
            return ("Indietro-Destra")
        else:
            alice.backward()
            return ("Indietro")
    elif dizionario_comandi["a"]:
        alice.left()
        return ("Sinistra")
    elif dizionario_comandi["d"]:
        alice.right()
        return ("Destra")

'''def esegui_comandi(command):
    if command == LISTA_COMANDI[0]:
        alice.forward()
        return ("Avanti")
    elif command == LISTA_COMANDI[1]:
        alice.backward()
        return ("Indietro")
    elif command == LISTA_COMANDI[2]:
        alice.left()
        return ("Sinistra")
    elif command == LISTA_COMANDI[3]:
        alice.right()
        return ("Destra")
    elif command == LISTA_COMANDI[4]:
        alice.stop()
'''

def controlla_ping():
    global ultimo_ping
    while True:
        cont = ultimo_ping
        time.sleep(3)
        if cont == ultimo_ping:
            alice.stop()
            break

def main():
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
        print(comando)
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
        if comando in LISTA_COMANDI:
            status = "ok"
            phrase = controllo_comandi(key, comando)
        else:
            phrase = f"{comando} non è presente in {LISTA_COMANDI}"
        key = None
        
        connection.sendall(f"{status}|{phrase}".encode())
    alice.stop()
    connection.close()
    s.close()

if __name__ == "__main__":
    main()

'''def hearthbeat_receive(receive_hearthbeat):
    socket_heartbeat.settimeout(6.5)
    while True:
        try:
            data = receive_heartbeat.recv(4092)
            print("up")
        except socket.timeout:
            print("FERMA TUTTO")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            break
        
    socket_hearthbeat.close()
    socket_command.close()'''
