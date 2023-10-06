# Simulador-MQTT
Um pequeno código em Python que simula um comunicador MQTT (Message Queuing Telemetry Transport). O MQTT é um protocolo de mensagens leve e amplamente utilizado para comunicação entre dispositivos na Internet das Coisas (IoT) e em outras aplicações de rede.

O código utiliza a biblioteca paho-mqtt, que é uma implementação Python do protocolo MQTT. Ele permite que os dispositivos publiquem mensagens em tópicos específicos e também se inscrevam em tópicos para receber mensagens de outros dispositivos.

## Como utilizar o código
Passo a passo para conseguir ver o código funcionar:
1. Baixar o Mosquitto (servidor MQTT)
2. Baixar a biblioteca paho-mqtt
3. Abrir o arquivo "MQTTpuro"

## Contexto do problema
### Simulador de tráfego
Para este projeto, considere uma cidade cujo formato é retangular, com ruas retas que vão de um
lado a outro. Ruas horizontais unem os lados esquerdo e direito da cidade, e as ruas verticais unem
os lados superior e inferior. Observe que quaisquer duas ruas são ou paralelas ou perpendiculares. As
ruas tem a mesma largura e possuem duas mãos de tráfego, onde cada mão tem apenas uma faixa.
Isto signica que não há ultrapassagens.
Nesta cidade circulam apenas carros autônomos sem motoristas. Os carros são controlados por
uma central de controle, e são usados para transportar pessoas pela cidade. As pessoas informam à
central de controle que precisam de transporte, indicando sua posição. A central então verica se há
um carro livre e o direciona para a localização da pessoa. Quando o carro chega a esta localização,
a pessoa informa o destino, que é comunicado à central de controle para direcionamento do carro.
Não há semáforos na cidade. Colisões são evitadas pela central de controle através do aumento
ou redução das velocidades dos carros.
Este projeto consiste da simulação do cenário acima com um certo número de carros e de pessoas.
Como dito acima, a simulação será em tempo discreto. Tome cuidado com a interação simultânea
entre a atualização dos carros e da central de controle pelo simulador e a comunicação entre os carros
e a central de controle. Use um objeto do tipo Lock (veja as aulas de programação paralela) em cada
carro e na central de controle para proteger o acesso dos dados internos de cada objeto.