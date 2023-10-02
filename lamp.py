import socket
import time
import random
import messages_pb2

EQUIPMENT_ID = "lamp001"
GATEWAY_IP = "127.0.0.1"
GATEWAY_PORT = 12345

lamp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lamp_socket.connect((GATEWAY_IP, GATEWAY_PORT))

lamp_state = messages_pb2.EquipmentState()
lamp_state.equipment_id = EQUIPMENT_ID

def send_state(state):
    message = state.SerializeToString()
    lamp_socket.send(message)

def toggle_lamp():
    lamp_state.is_on = not lamp_state.is_on
    send_state(lamp_state)

while True:
    # Simula uma alteração no estado da lâmpada a cada 5 segundos
    time.sleep(5)
    toggle_lamp()
