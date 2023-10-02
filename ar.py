import socket
import time
import random
import messages_pb2

EQUIPMENT_ID = "ac001"
GATEWAY_IP = "127.0.0.1"
GATEWAY_PORT = 12345

ac_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ac_socket.connect((GATEWAY_IP, GATEWAY_PORT))

ac_state = messages_pb2.EquipmentState()
ac_state.equipment_id = EQUIPMENT_ID

temperature_sensor = messages_pb2.TemperatureData()
temperature_sensor.equipment_id = EQUIPMENT_ID

def send_state(state):
    message = state.SerializeToString()
    ac_socket.send(message)

def send_temperature():
    temperature_sensor.temperature = random.uniform(18.0, 30.0)  # Simula temperatura entre 18°C e 30°C
    message = temperature_sensor.SerializeToString()
    ac_socket.send(message)

def toggle_ac():
    ac_state.is_on = not ac_state.is_on
    send_state(ac_state)

while True:
    # Simula uma alteração no estado do ar-condicionado a cada 10 segundos
    time.sleep(10)
    toggle_ac()

    # Simula o envio de dados de temperatura a cada 15 segundos quando o ar-condicionado está ligado
    if ac_state.is_on:
        time.sleep(5)  # Aguarda um pouco antes de enviar a temperatura pela primeira vez
        while ac_state.is_on:
            send_temperature()
            time.sleep(15)  # Simula o envio de temperatura a cada 15 segundos
