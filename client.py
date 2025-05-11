import socket
import threading

def recieve(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("Conexao encerrada")
            client.close()
            break

def main ():
    HOST = '127.0.0.1'
    PORT = 50000

    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    name = input('Informe seu nome de usuário:')
    client.send(str.encode(name))

    thread = threading.Thread(target=recieve, args=(client,))
    thread.start()

    while True: 
        message = input('Escreva sua mensagem')

        if message == '/exit':
            client.close()
            break
        client.send(str.encode(message))


if __name__ == "__main__":
    main()