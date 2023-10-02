import socket
import threading
import time
import messages_pb2  # Importe as classes geradas a partir do messages.proto

GATEWAY_IP = "127.0.0.1"  # IP do Gateway
GATEWAY_PORT = 12345  # Porta do Gateway para comunicação com os equipamentos

equipments = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((GATEWAY_IP, GATEWAY_PORT))
server_socket.listen(5)

print("Gateway iniciado. Aguardando conexões dos equipamentos...")

def discover_equipments():
    discovery_message = messages_pb2.EquipmentDiscovery()
    discovery_message.message = "Identify yourselves, intelligent devices!"

    # Implemente a lógica para enviar e receber mensagens de descoberta
    pass

def handle_equipment_connection(client_socket, address):
    equipment_type = None
    while True:
        try:
            # Recebe e desserializa a mensagem do equipamento
            data = client_socket.recv(1024)
            if not data:
                print(f"Conexão com {address} perdida.")
                break

            message = messages_pb2.EquipmentState()
            message.ParseFromString(data)

            # Se o tipo de equipamento ainda não foi definido, define-o
            if equipment_type is None:
                equipment_type = message.equipment_id

            # Verifica se o tipo da mensagem recebida corresponde ao tipo de equipamento esperado
            if message.equipment_id == equipment_type:
                print(f"Estado do {equipment_type} alterado para {'ligado' if message.is_on else 'desligado'}")
            else:
                print(f"Tipo de mensagem inesperado do equipamento {message.equipment_id}")

        except Exception as e:
            print(f"Erro ao lidar com a mensagem do equipamento {equipment_type}: {e}")
            break

def main():
    discovery_thread = threading.Thread(target=discover_equipments)
    discovery_thread.start()

    while True:
        client_socket, address = server_socket.accept()
        print(f"Conexão estabelecida com {address}")
        client_thread = threading.Thread(target=handle_equipment_connection, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    main()
