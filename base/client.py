import socket
SERVER_ADDRESS = ("localhost", 9090)
BUFFER_SIZE = 4096

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    s.sendall("Messaggio dal client".encode())
    messaggio = s.recv(BUFFER_SIZE)
    print(f"Ricevuto <{messaggio.decode()}> dal server")

    s.close()

if __name__ == "__main__":
    main()