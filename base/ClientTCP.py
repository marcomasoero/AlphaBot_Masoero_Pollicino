import socket
SERVER_ADDRESS = ("192.168.1.134", 9092)
BUFFER_SIZE = 4096

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    messaggio = s.recv(BUFFER_SIZE)
    print(messaggio.decode())
    
    while True:
        command = input ("Inserisci comando-> ")
        if command == "exit":
            s.sendall(f"{command}".encode())
            messaggio = s.recv(BUFFER_SIZE)
            print(messaggio.decode())
            break
        value = input("Inserisci il tempo-> ")
        s.sendall(f"{command}|{value}".encode())
        messaggio = s.recv(BUFFER_SIZE)
        print(messaggio.decode())

if __name__ == "__main__":
    main()