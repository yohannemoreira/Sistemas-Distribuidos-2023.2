import socket
import time
import messages_pb2

EQUIPMENT_ID = "tv001"
GATEWAY_IP = "127.0.0.1"
GATEWAY_PORT = 12345

tv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tv_socket.connect((GATEWAY_IP, GATEWAY_PORT))

tv_state = messages_pb2.EquipmentState()
tv_state.equipment_id = EQUIPMENT_ID

def send_state(state):
    message = state.SerializeToString()
    tv_socket.send(message)

def toggle_tv():
    while True:
        tv_state.is_on = not tv_state.is_on
        send_state(tv_state)
        print(f"Estado da TV alterado para {'ligado' if tv_state.is_on else 'desligado'}")
        time.sleep(7)  # Altera o estado da TV a cada 7 segundos

toggle_tv()
