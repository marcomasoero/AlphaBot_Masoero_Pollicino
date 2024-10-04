import socket
import AlphaBot

MY_ADDRESS = ("0.0.0.0", 9090)
BUFFER_SIZE = 4096
LISTA_COMANDI = ["w", "s", "a", "d", "release"]
alice = AlphaBot.AlphaBot()

def esegui_comandi(command):
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

def main():
    alice.stop()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    connection, client_address = s.accept() #bloccante
    print(f"Il client {client_address} si è connesso")
    message = (f"Comandi disponibili: {LISTA_COMANDI}")
    connection.sendall(message.encode())
    while True:
        message = connection.recv(BUFFER_SIZE) #bloccante
        comando = message.decode()
        print(comando)
        if comando == "esc":
            connection.sendall(f"comunicazione terminata".encode())
            break
        status = "error"
        if comando in LISTA_COMANDI:
            status = "ok"
            phrase = esegui_comandi(comando)
        else:
            phrase = f"{comando} non è presente in {LISTA_COMANDI}"
        
        connection.sendall(f"{status}|{phrase}".encode())
    connection.close()
    s.close()

if __name__ == "__main__":
    main()
