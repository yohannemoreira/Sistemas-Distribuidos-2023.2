import socket
import threading

clientes = {}
def handle_client(client_socket, address):
    new_user = False
    apelido = client_socket.recv(1024).decode('utf-8')
    while (new_user == False):
        if apelido in clientes.values():
            client_socket.send("Apelido já em uso.Tente novamente.".encode('utf-8'))
            client_socket.send("Digite seu apelido:".encode('utf-8'))
            apelido = client_socket.recv(1024).decode('utf-8')
        else:
            new_user = True
    clientes[client_socket] = apelido
    print(f"Novo cliente conectado: {apelido}")

    while True:
        mensagem = client_socket.recv(1024).decode('utf-8')
        if mensagem.startswith('/'):
            comando, *parametros = mensagem.split(' ')
            if comando == '/USUARIOS':
                lista_usuarios = ', '.join(clientes.values())
                client_socket.send(f'Usuários conectados: {lista_usuarios}'.encode('utf-8'))
            elif comando.startswith('/NICK'):
                apelido = ' '.join(parametros)
                if apelido in clientes.values():
                    client_socket.send("Apelido já em uso.".encode('utf-8'))
                else:
                    antigo_apelido = clientes[client_socket]
                    clientes[client_socket] = apelido
                    client_socket.send(f'Nick: {apelido}'.encode('utf-8'))
                    for client in clientes:
                        if client != client_socket:
                            client.send(f'{antigo_apelido} mudou seu apelido para {apelido}'.encode('utf-8'))
            elif comando == '/SAIR':
                del clientes[client_socket]
                for client in clientes:
                    client.send(f"{apelido} SAIU DO CHAT.".encode('utf-8'))
                    print(f"{apelido} saiu do chat.")
                client_socket.close()
                break
        else:
            for client in clientes:
                    if client != client_socket:
                        client.send(f'{clientes[client_socket]}: {mensagem}'.encode('utf-8'))

HOST = '127.0.0.1'
PORTA = 7777

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORTA))
servidor.listen(4)  # Aceita no máximo 4 conexões simultâneas

print(f"Servidor ouvindo em {HOST}: {PORTA}")

while True:
    client_socket, addr = servidor.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()