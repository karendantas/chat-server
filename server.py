import socket 
import threading

clients = {}
# um dicicionario com valor: nome e chave para um socket 

#verifico se o cliente nao esta tentando mandar uma messagem para si mesmo
#ou entao desconecto um cliente retirando ele do dict
def broadcast(message, sender = None):
    desconectd = []
    for name, client in clients.items():
        if name != sender:
            try:
                client.send(str.encode(message))
            except:
                client.close()
                desconectd.append(name)
    for name in desconectd:
        del clients[name]


def sendmessage(client):
    #recebendo o client e add ele no disct dos conectados
    name = client.recv(1024).decode()
    clients[name] = client

    broadcast(f'{name} entrou', sender=None)

    while True:
        try:
            message = client.recv(1024).decode()
            if message.startswith('@'):
                reciever, content = message[1:].split(" ", 1)
                if reciever in clients:
                    clients[reciever].send(f'de {name} para {reciever}: {content}'.encode())
                else:
                    client.send('Cliente não encontrado'.encode())
            else:
                broadcast(f'{name}: {message}', sender=None)


        except:
            client.close()
            del clients[name]
            broadcast(f"{name} saiu")
            break



def main ():
    HOST = '127.0.0.1'
    PORT = 50000

    s = socket.socket(family=socket.AF_INET, type= socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print('Servidor escutando em 127.0.0.1:50000')

    while True:
        client, addr = s.accept() #guardando conexao do client e endereço de uma conexao aceita
        thread = threading.Thread(target=sendmessage, args=(client, ))
        thread.start()

if __name__ == "__main__":
    main()
