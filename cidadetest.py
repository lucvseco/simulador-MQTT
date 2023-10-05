import matplotlib.pyplot as plt
import random

class Passageiro:
    def __init__(self, nome):
        self.nome = nome
        self.viagem_em_andamento = False
        self.destino = None

    def solicitar_viagem(self, central_controle):
        if not self.viagem_em_andamento:
            self.destino = random.choice(["A", "B", "C"])  # Destinos aleatórios
            central_controle.registrar_chamada(self)
            print(f"{self.nome} solicitou uma viagem para o destino {self.destino}")
        else:
            print(f"{self.nome} já está em uma viagem.")

    def atualizar(self, motorista):
        if self.viagem_em_andamento:
            print(f"{self.nome} está em uma viagem para {self.destino}.")
            if motorista.chegou_ao_destino(self.destino):
                print(f"{self.nome} chegou ao destino {self.destino}.")
                self.viagem_em_andamento = False

class Carro:
    def __init__(self, nome):
        self.nome = nome
        self.localizacao = "Base"
        self.em_viagem = False

    def atualizar(self):
        if self.em_viagem:
            print(f"{self.nome} está a caminho de {self.destino}.")
        else:
            print(f"{self.nome} está parado em {self.localizacao}.")

    def iniciar_viagem(self, destino):
        self.destino = destino
        self.em_viagem = True

    def chegou_ao_destino(self, destino):
        if self.em_viagem and self.destino == destino:
            self.em_viagem = False
            self.localizacao = destino
            return True
        return False

class CentralDeControle:
    def __init__(self):
        self.chamadas = []

    def registrar_chamada(self, passageiro):
        self.chamadas.append(passageiro)

    def atender_chamadas(self):
        if self.chamadas:
            passageiro = self.chamadas.pop(0)
            print(f"Central de Controle: Chamada de {passageiro.nome} atendida.")
            carro_disponivel = self.encontrar_carro_disponivel()
            if carro_disponivel:
                print(f"Central de Controle: Enviando carro para {passageiro.nome}.")
                carro_disponivel.iniciar_viagem(passageiro.destino)
                passageiro.viagem_em_andamento = True
            else:
                print("Central de Controle: Não há carros disponíveis no momento.")

    def encontrar_carro_disponivel(self):
        carros_disponiveis = [carro for carro in carros if not carro.em_viagem]
        if carros_disponiveis:
            return random.choice(carros_disponiveis)
        return None

# Criação de carros
carro1 = Carro("Carro 1")
carro2 = Carro("Carro 2")

# Criação de passageiros
passageiro1 = Passageiro("Passageiro 1")
passageiro2 = Passageiro("Passageiro 2")

# Lista de carros
carros = [carro1, carro2]

# Central de Controle
central_controle = CentralDeControle()

# Simulação
for _ in range(10):
    for passageiro in [passageiro1, passageiro2]:
        if random.random() < 0.3:
            passageiro.solicitar_viagem(central_controle)
    for carro in carros:
        carro.atualizar()
    central_controle.atender_chamadas()
    for passageiro in [passageiro1, passageiro2]:
        passageiro.atualizar(carro1)
        passageiro.atualizar(carro2)
    
class Viagem:
    def __init__(self, passageiro, destino):
        self.passageiro = passageiro
        self.destino = destino
        self.carro = None

    def atribuir_carro(self, carro):
        self.carro = carro

    def concluir_viagem(self):
        self.carro = None

# Coordenadas dos destinos da cidade
destinos = {
    "A": (0, 0),
    "B": (2, 4),
    "C": (4, 1),
}

# Função para plotar o mapa da cidade e os destinos
def plot_map(destinos, viagens_em_andamento):
    # ... (código anterior para plotar o mapa da cidade)

    # Plotar as viagens em andamento
    for viagem in viagens_em_andamento:
        coordenadas_carro = destinos[viagem.destino]
        plt.plot(coordenadas_carro[0], coordenadas_carro[1], 'bs')  # Ponto azul para representar o carro

# Criação de carros
carro1 = Carro("Carro 1")
carro2 = Carro("Carro 2")

# Criação de passageiros
passageiro1 = Passageiro("Passageiro 1")
passageiro2 = Passageiro("Passageiro 2")

# Lista de carros
carros = [carro1, carro2]

# Lista de viagens em andamento
viagens_em_andamento = []

# Central de Controle
central_controle = CentralDeControle()

# Função para atualizar o estado das viagens em andamento
def atualizar_viagens(viagens_em_andamento):
    viagens_concluidas = []
    for viagem in viagens_em_andamento:
        if not viagem.carro.em_viagem:
            viagem.passageiro.atualizar(viagem.carro)
            viagens_concluidas.append(viagem)
    for viagem in viagens_concluidas:
        viagens_em_andamento.remove(viagem)

# Simulação
for _ in range(10):
    for passageiro in [passageiro1, passageiro2]:
        if random.random() < 0.3:
            passageiro.solicitar_viagem(central_controle)
    for carro in carros:
        carro.atualizar()
    central_controle.atender_chamadas()

    # Verifique se há viagens concluídas e atualize o estado das viagens
    atualizar_viagens(viagens_em_andamento)

    for passageiro in [passageiro1, passageiro2]:
        if not passageiro.viagem_em_andamento:
            viagem = central_controle.encontrar_carro_disponivel(passageiro)
            if viagem:
                viagem.atribuir_carro(carro1)  # Pode ser atribuído a qualquer carro disponível
                viagens_em_andamento.append(viagem)
                print(f"Viagem iniciada: {passageiro.nome} para {viagem.destino}")

    # Plotar o mapa atualizado
    plot_map(destinos, viagens_em_andamento)

# Exibir o mapa final
plt.show()
