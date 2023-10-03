import paho.mqtt.client as mqtt
import time
import random

# Gerar um ID único para o passageiro (exemplo)
passenger_id = "passageiro123"

# Função de callback quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao servidor MQTT como passageiro.")
    else:
        print("Falha na conexão, código de retorno:", rc)

# Configurar o cliente MQTT do passageiro
client_passenger = mqtt.Client()
client_passenger.on_connect = on_connect

# Configurar o endereço do servidor MQTT (Mosquitto) e a porta
broker_address = "127.0.0.1"  # Substitua pelo endereço correto, se necessário
port = 1883                   # Porta padrão do MQTT

# Conectar-se ao servidor MQTT como passageiro
client_passenger.connect(broker_address, port)
client_passenger.loop_start()

# Função para gerar coordenadas de localização aleatórias
def generate_random_location():
    latitude = random.uniform(37.0, 38.0)  # Faixa de latitude de exemplo
    longitude = random.uniform(-122.0, -121.0)  # Faixa de longitude de exemplo
    return latitude, longitude

# Função para solicitar um carro com localização atual aleatória e destino fixo
def request_ride():
    latitude_atual, longitude_atual = generate_random_location()
    latitude_destino, longitude_destino = 37.8, -122.4  # Coordenadas fixas para o destino de exemplo
    topic = f"solicitacoes/{passenger_id}"
    message = f"Passageiro solicitou um carro de ({latitude_atual}, {longitude_atual}) para ({latitude_destino}, {longitude_destino})"
    client_passenger.publish(topic, message)

# Simulação de solicitação de carros (a cada 10 segundos)
while True:
    request_ride()
    time.sleep(10)
