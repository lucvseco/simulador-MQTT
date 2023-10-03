import paho.mqtt.client as mqtt
import time
import random

# IDs únicos para os carros (exemplo)
car_ids = ["carro001", "carro002", "carro003", "carro004", "carro005"]

# Função de callback quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao servidor MQTT como simulador de localização.")
    else:
        print("Falha na conexão, código de retorno:", rc)

# Configurar o cliente MQTT do simulador de localização
client_location_simulator = mqtt.Client()
client_location_simulator.on_connect = on_connect

# Configurar o endereço do servidor MQTT (Mosquitto) e a porta
broker_address = "127.0.0.1"  # Substitua pelo endereço correto, se necessário
port = 1883                   # Porta padrão do MQTT

# Conectar-se ao servidor MQTT como simulador de localização
client_location_simulator.connect(broker_address, port)
client_location_simulator.loop_start()

# Função para gerar coordenadas de localização aleatórias
def generate_random_location():
    latitude = random.uniform(37.0, 38.0)  # Faixa de latitude de exemplo
    longitude = random.uniform(-122.0, -121.0)  # Faixa de longitude de exemplo
    return latitude, longitude

# Simulação de atualização de localização dos carros (a cada 5 segundos)
while True:
    for car_id in car_ids:
        latitude_carro, longitude_carro = generate_random_location()
        topic = f"localizacao/{car_id}"
        message = f"Latitude: {latitude_carro}, Longitude: {longitude_carro}"
        client_location_simulator.publish(topic, message)
    time.sleep(5)
