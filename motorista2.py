import paho.mqtt.client as mqtt
import time

# Gerar um ID único para o motorista (exemplo)
driver_id = "motorista001"

# Função de callback quando a conexão é estabelecida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao servidor MQTT como motorista.")
        # Assine o tópico de solicitações para motoristas
        client.subscribe("solicitacoes/+")
    else:
        print("Falha na conexão, código de retorno:", rc)

# Função de callback quando uma mensagem é recebida em um tópico assinado
def on_message(client, userdata, message):
    passenger_id = message.topic.split("/")[1]
    print(f"Motorista {driver_id} recebeu solicitação do passageiro {passenger_id}: {message.payload.decode('utf-8')}")
    latitude_atual, longitude_atual, latitude_destino, longitude_destino = extract_coordinates(message.payload.decode('utf-8'))
    # Calcule o trajeto e siga-o
    simulate_ride(driver_id, latitude_atual, longitude_atual, latitude_destino, longitude_destino)

# Configurar o cliente MQTT do motorista
client_driver = mqtt.Client()
client_driver.on_connect = on_connect
client_driver.on_message = on_message

# Configurar o endereço do servidor MQTT (Mosquitto) e a porta
broker_address = "127.0.0.1"  # Substitua pelo endereço correto, se necessário
port = 1883                   # Porta padrão do MQTT

# Conectar-se ao servidor MQTT como motorista
client_driver.connect(broker_address, port)
client_driver.loop_start()

# Função para extrair as coordenadas da mensagem do passageiro
def extract_coordinates(message):
    parts = message.split()
    if len(parts) == 4 and parts[0] == "Passageiro" and parts[2] == "para":
        return float(parts[3].replace("(", "").replace(")", "").split(",")[0]), float(parts[3].replace("(", "").replace(")", "").split(",")[1]), float(parts[5].replace("(", "").replace(")", "").split(",")[0]), float(parts[5].replace("(", "").replace(")", "").split(",")[1])
    return None, None, None, None

# Função para simular o trajeto do motorista
def simulate_ride(driver_id, latitude_atual, longitude_atual, latitude_destino, longitude_destino):
    while True:
        # Simule o movimento do carro em direção ao destino
        if latitude_atual == latitude_destino and longitude_atual == longitude_destino:
            print(f"Motorista {driver_id} chegou ao destino.")
            break
        else:
            # Calcule a próxima posição (simplificação para movimento linear)
            step = 0.001  # Apenas uma simulação
            if latitude_atual < latitude_destino:
                latitude_atual += step
            elif latitude_atual > latitude_destino:
                latitude_atual -= step
            if longitude_atual < longitude_destino:
                longitude_atual += step
            elif longitude_atual > longitude_destino:
                longitude_atual -= step
            print(f"Motorista {driver_id} está em ({latitude_atual}, {longitude_atual}).")
        time.sleep(1)

# Mantenha o programa em execução para receber mensagens
while True:
    time.sleep(1)
