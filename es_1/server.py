import socket
import AlphaBot
import time

MY_ADDRESS = ("0.0.0.0", 9092)
BUFFER_SIZE = 4096
LISTA_COMANDI = ["forward", "backward", "left", "right"]
alice = AlphaBot.AlphaBot()


def esegui_comandi(command, value):
    if command == LISTA_COMANDI[0]:
        alice.forward()
        time.sleep(value)
        alice.stop()
        return (f"Sono andato avanti per {value}")
    elif command == LISTA_COMANDI[1]:
        alice.backward()
        time.sleep(value)
        alice.stop()
        return (f"Sono andato indietro per {value}")
    elif command == LISTA_COMANDI[2]:
        alice.left()
        time.sleep(value)
        alice.stop()
        return (f"Ho ruotato verso sinistra per {value}")
    elif command == LISTA_COMANDI[3]:
        alice.right()
        time.sleep(value)
        alice.stop()
        return (f"Ho ruotato verso destra per {value}")

def controlla_numero(string):
    lista_numeri = "0123456789"
    punto = False
    if string == '':
        return False
    for char in string:
        if char not in lista_numeri:
            if char == '.':
                if punto == True:
                    return False
                punto = True
            else:
               return False
    return True

def main():
    alice.stop()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    connection, client_address = s.accept() #bloccante
    print(f"Il client {client_address} si è connesso")
    message = (f"Comandi disponibili: {LISTA_COMANDI}\ntempo in secondi")
    connection.sendall(message.encode())
    while True:
            message = connection.recv(BUFFER_SIZE) #bloccante
            mes_dec = message.decode()
            print(mes_dec)
            if mes_dec == "exit":
                connection.sendall(f"comunicazione terminata".encode())
                break
            if '|' not in mes_dec:
                connection.sendall("il messagio deve essere {command}|{value}".encode())
            else:
                command, value = mes_dec.split('|')
                if controlla_numero(value) == False:
                    connection.sendall("il valore deve essere un numero".encode())
                else:
                    value = float(value)
                    status = "error"
                    if command in LISTA_COMANDI:
                        status = "ok"
                        phrase = esegui_comandi(command, value)
                    else:
                        phrase = f"{command} non è presente in {LISTA_COMANDI}"
                    
                    connection.sendall(f"{status}|{phrase}".encode())
    connection.close()
    s.close()

if __name__ == "__main__":
    main()