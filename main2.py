import random
import time

class Pessoa:
    def __init__(self, nome, posicao_atual, destino):
        self.nome = nome
        self.posicao_atual = posicao_atual
        self.destino = destino
        self.comunicacao = comunicacao

class Carro:
    def __init__(self, placa):
        self.placa = placa
        self.velocidade = 0
        self.posicao = (0, 0)
        self.comunicacao = comunicacao

    def mudar_velocidade(self, nova_velocidade):
        self.velocidade = nova_velocidade
        
    def enviar_informacoes(self):
        origem = self.posicao
        destino = self.destino
        velocidade = self.velocidade
        posicao = self.posicao
        self.comunicacao.enviar_informacoes(origem, destino, velocidade, posicao)
        return self.velocidade, self.posicao

    def mover(self, nova_posicao):
           if not self.estacionado:
            self.posicao = nova_posicao
            self.enviar_informacoes()  # Envia informações ao mover

            # Verifica se chegou ao destino
            if self.posicao == self.destino:
                self.chegar_destino()
            else:
                print(f"O carro {self.placa} está estacionado e não pode se mover.")
            
    def chegar_destino(self):
        self.estacionado = True
        
class comunicacao:
    def enviar_informacoes(self, origem, destino, velocidade, posicao):
        # Implemente aqui a lógica de envio de informações para a central de controle
        pass

    def receber_comando_velocidade(self):
        # Implemente aqui a lógica para receber o comando de mudança de velocidade
        pass

    def receber_novo_destino(self):
        # Implemente aqui a lógica para receber o novo destino da central de controle
        pass

    def enviar_mensagem(self, destino, mensagem):
        # Implemente aqui a lógica de envio de mensagem para um destino específico
        pass
    
class ComunicacaoMQTT(comunicacao):
    def enviar_informacoes(self, origem, destino, velocidade, posicao):
        # Implemente aqui a lógica de envio via MQTT
        pass

    def receber_comando_velocidade(self):
        # Implemente aqui a lógica de recebimento via MQTT
        pass

    def receber_novo_destino(self):
        # Implemente aqui a lógica de recebimento de novo destino via MQTT
        pass

    def enviar_mensagem(self, destino, mensagem):
        # Implemente aqui a lógica de envio de mensagem via MQTT
        pass
    
class ComunicacaoChamadaFuncao(comunicacao):
    def enviar_informacoes(self, origem, destino, velocidade, posicao):
        # Implemente aqui a lógica de envio via chamada de função
        pass

    def receber_comando_velocidade(self):
        # Implemente aqui a lógica de recebimento via chamada de função
        pass

    def receber_novo_destino(self):
        # Implemente aqui a lógica de recebimento de novo destino via chamada de função
        pass

    def enviar_mensagem(self, destino, mensagem):
        # Implemente aqui a lógica de envio de mensagem via chamada de função
        pass


class CentralControle:
    def __init__(self):
        self.carros = []
        self.pessoas = []
        
        # Adicionando listas para armazenar histórico
        self.historico_velocidade = []
        self.historico_posicao = []

    def cadastrar_carro(self, carro):
        self.carros.append(carro)

    def cadastrar_pessoa(self, pessoa):
        self.pessoas.append(pessoa)

    def enviar_pedido(self, pessoa):
        carro_disponivel = self.encontrar_carro_disponivel()
        if carro_disponivel:
            self.enviar_carro(carro_disponivel, pessoa)
        self.comunicacao.enviar_pedido(self)

    def enviar_carro(self, carro, pessoa):
        # Implemente a lógica de cálculo de rota aqui
        
        if carro.velocidade == 0:
            rota = self.calcular_rota(carro.posicao, pessoa.posicao_atual)
            carro.mover(pessoa.posicao_atual)
            pessoa.destino = (random.randint(0, 100), random.randint(0, 100))  # Exemplo de destino aleatório
            carro.mover(pessoa.destino)
            self.enviar_rota(carro, rota)
            carro.chegar_destino()

            # Após o carro chegar ao destino, mudar a velocidade
            nova_velocidade = random.randint(30, 120)  # Exemplo de nova velocidade aleatória
            carro.mudar_velocidade(nova_velocidade)
        else:
            print(f"O carro {carro.placa} não está disponível no momento.")
            
        # Após mover o carro, registrar a posição e velocidade
        self.historico_velocidade.append(carro.velocidade)
        self.historico_posicao.append(carro.posicao)

    def encontrar_carro_disponivel(self):
        # Implemente a lógica para encontrar um carro disponível
        carros_disponiveis = [carro for carro in self.carros if carro.velocidade == 0]
        if carros_disponiveis:
            return carros_disponiveis[0]
        else:
            return None
    
    def mudar_velocidade_carro(self, carro, nova_velocidade):
        carro.mudar_velocidade(nova_velocidade)


def calcular_rota(origem, destino):
    # Implemente a lógica de cálculo de rota aqui
    return []  # Retornar a lista de coordenadas da rota

if __name__ == "__main__":
    central = CentralControle()

    num_carros = 5
    num_pessoas = 10

    # Cadastrar carros
    for i in range(num_carros):
        carro = Carro(id=i)
        central.cadastrar_carro(carro)

    # Cadastrar pessoas
    for i in range(num_pessoas):
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