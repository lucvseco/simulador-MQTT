import matplotlib.pyplot as plt
import random
import paho.mqtt.client as mqtt

class Passageiro:
    def __init__(self, nome, mqtt_broker_host, mqtt_broker_port):
        self.nome = nome
        self.viagem_em_andamento = False
        self.destino = None
        self.tempo_restante = 0
        self.mqtt_client = mqtt.Client(f"Passageiro_{nome}")
        self.mqtt_client.connect(mqtt_broker_host, mqtt_broker_port)
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.subscribe(f"passageiro/{self.nome}")
        self.mqtt_client.on_connect = self.on_passageiro_connect
        self.mqtt_client.loop_start()

    def solicitar_viagem(self, central_controle, tempo_atual):
        if not self.viagem_em_andamento:
            self.destino = random.choice(["A", "B", "C"])
            self.tempo_restante = random.randint(1, 5)
            central_controle.registrar_chamada(self, tempo_atual)
            message = f"{self.nome} solicitou uma viagem para o destino {self.destino} em t = {tempo_atual}."
            self.mqtt_client.publish(f"passageiro/{self.nome}", message)
        else:
            print(f"{self.nome} já está em uma viagem.")

    def atualizar(self, motorista):
        if self.viagem_em_andamento:
            print(f"{self.nome} está em uma viagem para {self.destino}.")
            if motorista.chegou_ao_destino(self.destino):
                print(f"{self.nome} chegou ao destino {self.destino}.")
                self.viagem_em_andamento = False

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        # Processar a mensagem recebida, se necessário

    def on_passageiro_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Passageiro {client._client_id.decode()} conectado com sucesso ao servidor MQTT.")
            # Enviar uma mensagem de boas-vindas para o passageiro conectado
            mensagem_de_boas_vindas = "Bem-vindo ao sistema de carros!"
            client.publish("passageiro/boas-vindas", mensagem_de_boas_vindas)
        else:
            print(f"Falha na conexão do passageiro {client._client_id.decode()} ao servidor MQTT, código de retorno: {rc}")

class Carro:
    def __init__(self, nome):
        self.nome = nome
        self.localizacao = "Base"
        self.em_viagem = False
        self.tempo_restante = 0

    def atualizar(self, tempo_atual):
        if self.em_viagem:
            print(f"{self.nome} está a caminho de {self.destino}.")
            self.tempo_restante -= 1
            if self.tempo_restante == 0:
                self.em_viagem = False
                self.localizacao = self.destino
        else:
            print(f"{self.nome} está parado em {self.localizacao} em t = {tempo_atual}.")

    def iniciar_viagem(self, destino, tempo_atual):
        self.destino = destino
        self.em_viagem = True
        self.tempo_restante = random.randint(1, 5)
        print(f"{self.nome} iniciou a viagem para {destino} em t = {tempo_atual}.")

    def chegou_ao_destino(self, destino):
        return self.em_viagem and self.destino == destino

class CentralDeControle:
    def __init__(self):
        self.chamadas = []

    def registrar_chamada(self, passageiro, tempo_atual):
        self.chamadas.append((passageiro, tempo_atual))

    def atender_chamadas(self, tempo_atual):
        chamadas_atuais = list(self.chamadas)
        for passageiro, tempo_chamada in chamadas_atuais:
            if tempo_atual - tempo_chamada >= random.randint(1, 5):
                self.chamadas.remove((passageiro, tempo_chamada))
                if not passageiro.viagem_em_andamento:
                    carro_disponivel = self.encontrar_carro_disponivel()
                    if carro_disponivel:
                        print(f"Central de Controle: Enviando carro para {passageiro.nome} em t = {tempo_atual}.")
                        carro_disponivel.iniciar_viagem(passageiro.destino, tempo_atual)
                        passageiro.viagem_em_andamento = True
                    else:
                        print(f"Central de Controle: Não há carros disponíveis para {passageiro.nome} em t = {tempo_atual}.")

    def encontrar_carro_disponivel(self):
        carros_disponiveis = [carro for carro in carros if not carro.em_viagem]
        if carros_disponiveis:
            return random.choice(carros_disponiveis)
        return None

class Viagem:
    def __init__(self, passageiro, destino, tempo_atual):
        self.passageiro = passageiro
        self.destino = destino
        self.carro = None
        self.tempo_iniciada = tempo_atual

    def atribuir_carro(self, carro):
        self.carro = carro

    def concluir_viagem(self, tempo_atual):
        self.carro = None
        print(f"Viagem concluída para {self.passageiro.nome} para {self.destino} em t = {tempo_atual}.")

destinos = {
    "A": (0, 0),
    "B": (2, 4),
    "C": (4, 1),
}

tamanho_quarteirao = 1.0
quarteiroes = [(x, y) for x in range(6) for y in range(6)]

def plot_map(destinos, viagens_em_andamento):
    plt.figure()

    # Plotar os quarteirões da cidade
    for x, y in quarteiroes:
        plt.plot([x, x + tamanho_quarteirao], [y, y], 'k-', lw=0.5)
        plt.plot([x, x + tamanho_quarteirao], [y + tamanho_quarteirao, y + tamanho_quarteirao], 'k-', lw=0.5)
        plt.plot([x, x], [y, y + tamanho_quarteirao], 'k-', lw=0.5)
        plt.plot([x + tamanho_quarteirao, x + tamanho_quarteirao], [y, y + tamanho_quarteirao], 'k-', lw=0.5)

    # Plotar os destinos da cidade
    for destino, coordenadas in destinos.items():
        plt.plot(coordenadas[0], coordenadas[1], 'ro')  
        plt.text(coordenadas[0], coordenadas[1], destino, fontsize=12, ha='right')

    # Plotar passageiros
    for viagem in viagens_em_andamento:
        if viagem.passageiro.viagem_em_andamento:
            plt.plot(viagem.passageiro.localizacao[0], viagem.passageiro.localizacao[1], 'go') 

    # Plotar carros
    for carro in carros:
        plt.plot(carro.localizacao[0], carro.localizacao[1], 'bs')  
        plt.text(carro.localizacao[0], carro.localizacao[1], carro.nome, fontsize=12, ha='right')

    plt.xlim(-1, 6)
    plt.ylim(-1, 6)

    # Configurar rótulos e título
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    plt.title("Mapa")

    # Exibir o mapa
    plt.grid(True)
    plt.show()

mqtt_broker_host = "127.0.0.1"  # Host do broker MQTT (Mosquitto)
mqtt_broker_port = 1883  # Porta do broker MQTT (Padrão é 1883)

# Função para atualizar o estado das viagens em andamento
def atualizar_viagens(viagens_em_andamento, tempo_atual):
    viagens_concluidas = []
    for viagem in viagens_em_andamento:
        if not viagem.carro.em_viagem:
            viagem.passageiro.atualizar(viagem.carro)
            viagens_concluidas.append(viagem)
    for viagem in viagens_concluidas:
        viagem.concluir_viagem(tempo_atual)
        viagens_em_andamento.remove(viagem)

# Função para encontrar uma viagem disponível para um passageiro
def encontrar_viagem_disponivel(passageiro, tempo_atual):
    if not passageiro.viagem_em_andamento:
        for destino in destinos:
            viagem = Viagem(passageiro, destino, tempo_atual)
            viagem_disponivel = True
            for viagem_em_andamento in viagens_em_andamento:
                if viagem_em_andamento.destino == destino:
                    viagem_disponivel = False
                    break
            if viagem_disponivel:
                return viagem
    return None

# Configurar carros e passageiros
carro1 = Carro("Carro 1")
carro2 = Carro("Carro 2")
carros = [carro1, carro2]

passageiro1 = Passageiro("Passageiro 1", mqtt_broker_host, mqtt_broker_port)
passageiro2 = Passageiro("Passageiro 2", mqtt_broker_host, mqtt_broker_port)

viagens_em_andamento = []
central_controle = CentralDeControle()

# Simulação em tempo discreto
tempo_atual = 0
for _ in range(10):
    tempo_atual += 1  

    for passageiro in [passageiro1, passageiro2]:
        if random.random() < 0.3:
            passageiro.solicitar_viagem(central_controle, tempo_atual)

    for carro in carros:
        carro.atualizar(tempo_atual)

    central_controle.atender_chamadas(tempo_atual)

    atualizar_viagens(viagens_em_andamento, tempo_atual)

    for passageiro in [passageiro1, passageiro2]:
        if not passageiro.viagem_em_andamento:
            viagem = encontrar_viagem_disponivel(passageiro, tempo_atual)
            if viagem:
                viagem.atribuir_carro(carro1)  
                viagens_em_andamento.append(viagem)
                print(f"Viagem iniciada: {passageiro.nome} para {viagem.destino} em t = {tempo_atual}")

    # Atualizar a localização de passageiros e carros nos quarteirões
    for passageiro in [passageiro1, passageiro2]:
        passageiro.localizacao = random.choice(quarteiroes)
    for carro in carros:
        if carro.em_viagem:
            carro.localizacao = random.choice(quarteiroes)

    # Plotar o mapa atualizado
    plot_map(destinos, viagens_em_andamento)

plt.show()
