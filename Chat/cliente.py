import socket
import threading

comando = ''
sair_lopp = False
cliente = socket
apelido_autorizado = False


def receber_mensagens(sock):
    while True:
        try:
            mensagem = sock.recv(1024).decode('utf-8')
        except ConnectionAbortedError:
            print("Você saiu do servidor.")
            cliente.close()
            exit()

        print(mensagem)


print("""
██████  ███████ ███    ███     ██    ██ ██ ███    ██ ██████   ██████  
██   ██ ██      ████  ████     ██    ██ ██ ████   ██ ██   ██ ██    ██ 
██████  █████   ██ ████ ██     ██    ██ ██ ██ ██  ██ ██   ██ ██    ██ 
██   ██ ██      ██  ██  ██      ██  ██  ██ ██  ██ ██ ██   ██ ██    ██ 
██████  ███████ ██      ██       ████   ██ ██   ████ ██████   ██████  
                                                                      
                                                                      
""")
while sair_lopp == False:
    comando = input("Digite /ENTRAR para entrar no servidor: ")
    if comando == '/ENTRAR':
        HOST = input("Digite o IP do servidor: ")
        PORTA = int(input("Digite a porta do servidor: "))
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cliente.connect((HOST, PORTA))
            sair_lopp = True
            apelido = input("Digite seu apelido: ")
            cliente.send(apelido.encode('utf-8'))

        except Exception as error:
            print(f"Não foi possível entrar no servidor. IP ou Porta incorretos!")
            tentativa = input("Digite 'S' para tentar novamente ou qualquer letra para encerrar:")
            if tentativa != 'S':
                print("""
████████  ██████ ██   ██  █████  ██    ██ 
   ██    ██      ██   ██ ██   ██ ██    ██ 
   ██    ██      ███████ ███████ ██    ██ 
   ██    ██      ██   ██ ██   ██ ██    ██ 
   ██     ██████ ██   ██ ██   ██  ██████  
                                          
                                          
                                  """)
                exit()

    else:
        print("Comando inválido")

thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente,))
thread_recebimento.start()

while True:
    mensagem = input()
    cliente.send(mensagem.encode('utf-8'))

    if mensagem == '/SAIR':
        cliente.close()
        exit()