import random
import time

class Pessoa:
    def __init__(self, nome, posicao_atual, destino):
        self.nome = nome
        self.posicao_atual = posicao_atual
        self.destino = destino

class Carro:
    def __init__(self, placa):
        self.placa = placa
        self.velocidade = 0
        self.posicao = (0, 0)

    def mover(self, nova_posicao, nova_velocidade):
        self.posicao = nova_posicao
        self.velocidade = nova_velocidade

class CentralControle:
    def __init__(self):
        self.carros = []
        self.pessoas = []

    def cadastrar_carro(self, carro):
        self.carros.append(carro)

    def cadastrar_pessoa(self, pessoa):
        self.pessoas.append(pessoa)

    def enviar_pedido(self, pessoa):
        carro_disponivel = self.encontrar_carro_disponivel()
        if carro_disponivel:
            self.enviar_carro(carro_disponivel, pessoa)

    def enviar_carro(self, carro, pessoa):
        # Implemente a lógica de cálculo de rota aqui
        rota = calcular_rota(carro.posicao, pessoa.posicao)
        carro.mover(pessoa.posicao, velocidade=60)
        pessoa.destino = (random.randint(0, 100), random.randint(0, 100))  # Exemplo de destino aleatório
        carro.mover(pessoa.destino, velocidade=60)

    def encontrar_carro_disponivel(self):
        # Implemente a lógica para encontrar um carro disponível
        carros_disponiveis = [carro for carro in self.carros if carro.velocidade == 0]
        if carros_disponiveis:
            return carros_disponiveis[0]
        else:
            return None

def calcular_rota(origem, destino):
    # Implemente a lógica de cálculo de rota aqui
    return []  # Retornar a lista de coordenadas da rota

if __name__ == "__main__":
    central = CentralControle()

    # Cadastrar carros
    for i in range(5):
        carro = Carro(id=i)
        central.cadastrar_carro(carro)

    # Cadastrar pessoas
    for i in range(10):
        pessoa = Pessoa(nome=f"Pessoa {i}", posicao_atual=(random.randint(0, 100), random.randint(0, 100)), destino=None)
        central.cadastrar_pessoa(pessoa)
        central.enviar_pedido(pessoa)

    # Simulação de movimento dos carros
    while True:
        for carro in central.carros:
            if carro.velocidade > 0:
                # Simulação de movimento
                nova_posicao = (carro.posicao[0] + 1, carro.posicao[1] + 1)  # Exemplo de movimento simples
                carro.mover(nova_posicao, nova_velocidade=60)
                print(f"Carro {carro.id} se moveu para {nova_posicao}")
        time.sleep(1)
