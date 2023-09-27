import tkinter as tk
import random
import time
import threading

# Configurações da cidade
largura_cidade = 500
altura_cidade = 500

# Configurações das pistas
num_pistas_horizontais = 3
num_pistas_verticais = 4
cor_pista = "black"  # Cor das pistas

# Configurações dos carros
carros = []
num_carros = 5

# Função para mover os carros ao longo das pistas
def mover_carros():
    while True:
        for carro in carros:
            x, y, speed_x, speed_y, retangulo = carro
            x += speed_x
            
            # Limitar o movimento na direção X para permanecer dentro das pistas
            if x < espacamento_x:
                x = espacamento_x
                speed_x = -speed_x  # Inverte a direção ao atingir a borda esquerda
            elif x > largura_cidade - espacamento_x - 30:
                x = largura_cidade - espacamento_x - 30
                speed_x = -speed_x  # Inverte a direção ao atingir a borda direita
            
            canvas.move(retangulo, x - carro[0], 0)  # Movimento apenas na direção X
            carro[0] = x
            carro[2] = speed_x
            canvas.update()
            time.sleep(0.1)

# Função para criar um novo carro
def criar_carro():
    # Calcula coordenadas aleatórias dentro das pistas
    x = random.randint(espacamento_x + 3, largura_cidade - espacamento_x - 30 - 3)
    y = random.randint(espacamento_y + 3, altura_cidade - espacamento_y - 15 - 3)
    
    # Arredonda as coordenadas para a grade formada pelas linhas pretas
    x = round(x / espacamento_x) * espacamento_x
    y = round(y / espacamento_y) * espacamento_y
    
    retangulo = canvas.create_rectangle(x, y, x + 30, y + 15, fill="blue")
    speed_x = random.choice([1, -1, 0])
    speed_y = random.choice([1, -1, 0])
    carros.append([x, y, speed_x, speed_y, retangulo])
    
# Configurar a janela principal
root = tk.Tk()
root.title("Simulador de Tráfego")

# Calcular o espaçamento entre as pistas
espacamento_x = largura_cidade // (num_pistas_verticais + 1)
espacamento_y = altura_cidade // (num_pistas_horizontais + 1)

# Criar o canvas da cidade
canvas = tk.Canvas(root, width=largura_cidade, height=altura_cidade)
canvas.pack()

# Criar pistas horizontais com linhas mais grossas
for i in range(1, num_pistas_horizontais + 1):
    y = i * espacamento_y
    canvas.create_rectangle(espacamento_x, y - 2, largura_cidade - espacamento_x, y + 15, fill=cor_pista)

# Criar pistas verticais com linhas mais grossas
for i in range(1, num_pistas_verticais + 1):
    x = i * espacamento_x
    canvas.create_rectangle(x - 2, espacamento_y, x + 15, altura_cidade - espacamento_y, fill=cor_pista)

# Iniciar thread para mover os carros
carros_thread = threading.Thread(target=mover_carros)
carros_thread.start()

# Botão para adicionar carros
botao_adicionar_carro = tk.Button(root, text="Adicionar Carro", command=criar_carro)
botao_adicionar_carro.pack()

# Botão para sair
botao_sair = tk.Button(root, text="Sair", command=root.destroy)
botao_sair.pack()

root.mainloop()