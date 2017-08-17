import tkinter as tk
from datetime import datetime
from math import sqrt, pi, log10

import numpy as np
import pygame


def get_monitor_size():
    """
    Método que identifica o tamanho da tela do computador.
    :return: Retorna os valores de largura e altura.
    """
    root = tk.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()


WIDTH = get_monitor_size()[0] - 100  # Retira 100pxs para folga
HEIGHT = get_monitor_size()[1] - 100  # Retira 100pxs para folga
CHANNEL = 9

COLORS = [
    (214, 42, 42),
    (223, 0, 0),
    (255, 15, 0),
    (255, 93, 0),
    (255, 144, 0),
    (255, 186, 14),
    (255, 255, 49),
    (255, 249, 156),
    (179, 223, 244),
    (126, 202, 239),
    (28, 191, 251),
    (15, 163, 255),
    (38, 131, 246),
    (63, 105, 226),
    (22, 42, 244),
    (54, 12, 249)
]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Inicia o PyGame
pygame.init()


def draw_line(x1, y1, x2, y2):
    pygame.draw.line(DISPLAYSURF, color, (x1, y1), (x2, y2))


def draw_point(color, x, y):
    pygame.draw.line(DISPLAYSURF, color, (x, y), (x, y))


def calc_distance(x1, y1, x2, y2):
    """
    Método responsável por realizar o calculo da distância entre dois pontos no plano cartesiano.
    :param x1: Valor de X no ponto 1.
    :param y1: Valor de Y no ponto 1.
    :param x2: Valor de X no ponto 2.
    :param y2: Valor de Y no ponto 2.
    :return: Retorna um valor float representando a distância dos pontos informados.
    """
    return sqrt(pow((x1 - x2), 2.0) + pow((y1 - y2), 2.0))


def get_access_point_position():
    # return [1000, 450]
    # return [0, 0]
    # return [100, 900]
    return [159, 357]


def frequency():
    """
    Calcula a frequência de acordo com o canal
    :return: Frequência do canal
    """
    return (2.407 + (5 * CHANNEL) / 1000) * 10 ** 9


def wave_length():
    """
    Velocidade da luz / frequência do canal
    """
    C = 299792458
    return C / frequency()


def path_loss(d):
    """
    Perda no caminho (Path Loss) mensurado em dB
    :param d: Distâcia
    :return: Perda no caminho
    """
    return 20 * log10((4 * pi * d) / wave_length())


def two_ray_ground_reflection_model(Pt, Gt, Gr, Ht, Hr, d, L):
    """
    Pr
    """
    return (Pt * Gt * Gr * pow(Ht, 2) * pow(Hr, 2)) / (pow(d, 4) * L)


def free_space_model(Pt, Gt, Gr, lamb, d, L):
    """
    Pr
    """
    return (Pt * Gt * Gr * (pow(lamb, 2))) / (pow((4 * pi), 2) * pow(d, 2) * L)


def log_distance(d0, d, gamma):
    """
    Modelo logaritmo de perda baseado em resultados experimentais. Independe da frequência do sinal transmitido
    e do ganho das antenas transmissora e receptora
    :param d0: Distância do ponto de referência d0
    :param d:
    :param gamma: Valor da constante de propagação que difere para cada tipo de ambiente.
    :return:
    """
    # return path_loss(d) + 10 * gamma * log10(d / d0)
    return 17 - (60 + 10 * gamma * log10(d / d0))  # igual está na tabela


def propagation_model(x, y):
    access_point = get_access_point_position()
    d = calc_distance(x, y, access_point[0], access_point[1])
    if d == 0:
        d = 1
    gamma = 5

    return log_distance(1, d, gamma)


def print_matriz(matriz):
    """
    Método responsável por imprimir a matriz em um arquivo
    :param matriz: Matriz N x M
    :return: None
    """
    print("Escrevendo matriz no arquivo de saida...")
    print("Dimanções na matriz: " + str(np.shape(matriz)))
    f = open('saida_passo_01', 'w')
    for linha in matriz:
        for valor in linha:
            f.write(str(valor) + "\t")
        f.write('\n')
    f.close()
    print("Matriz salva no arquivo.")


def get_percentage_of_range(min, max, x):
    """
    Método responsável por retornar a porcentagem de acordo com um respectivo intervalo
    :param min: Valor mínimo do intervalo
    :param max: Valor máximo do intervalo
    :param x: Valor que está no intervalo de min-max que deseja saber sua respectiva porcentagem
    :return: Retorna uma porcentagem que está de acordo com o intervalo min-max
    """
    return ((x - min) / (max - min)) * 100


def get_value_in_list(percent, list):
    """
    Método retorna o valor de uma posição de uma lista. A posição é calculada de acordo a porcentagem.
    :param percent: Valor float representando a porcentagem
    :param list: Lista com n números
    :return: Retorna o valor da posição calculada
    """
    position = (percent / 100) * len(list)
    if position < 1:
        position = 1
    elif position >= len(list):
        position = len(list)
    return list[int(position - 1)]


def get_color_of_interval(min, max, x):
    """
    Este método retorna uma cor de acordo com o valor que está entre o intervalo min-max. Em outras palavras,
    este método transforma um número em uma cor dentro de uma faixa informada.
    :param min: Valor mínimo do intervalo
    :param max: Valor máximo do intervalo
    :param x: Valor que está dentro do intervalo e que deseja saber sua cor
    :return: Retorna uma tupla representando um cor no formato RGB.
    """
    percentage = get_percentage_of_range(min, max, x)
    color = get_value_in_list(percentage, COLORS)
    # print('Color: ' + str(color))
    return color


print("Iniciando simulação.")

# Marca o inicio da simulação
inicio = datetime.now()

# Configura o tamanho da janela
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Simulando...')

# Cria uma matriz para guardar os resultados calculados
matrix_results = np.zeros(shape=(WIDTH, HEIGHT))

print("Posição do access point: " + str(get_access_point_position()))

# Preenche a matriz de resultados usando um modelo de propagação
for x in range(WIDTH):
    for y in range(HEIGHT):
        value = propagation_model(x, y)
        matrix_results[x][y] = value

# Guarda os valores máximo e mínimo da matriz
matrix_max_value = matrix_results.max()
matrix_min_value = matrix_results.min()

# Lê os valores da matriz que contêm valores calculados e colore
for x in range(WIDTH):
    for y in range(HEIGHT):
        color = get_color_of_interval(matrix_min_value, matrix_max_value, matrix_results[x][y])
        draw_point(color, x, y)

# Pinta de vermelho a posição do Access Point
ap = get_access_point_position()
draw_point(RED, ap[0], ap[1])

# Atualiza a janela do PyGame para que exiba a imagem
pygame.display.update()
# Grava os valores da matriz no arquivo
print_matriz(matrix_results)

# Marca o fim da simulação
fim = datetime.now()

print("\nInicio: \t" + str(inicio.time()))
print("Fim: \t\t" + str(fim.time()))
print("Duração: \t" + str((fim - inicio).seconds) + " segundos.\n")

pygame.display.set_caption('Simulação terminada')
print('Simulação terminada.')

print("Maior valor da matriz: " + str(matrix_max_value))
print("Menor valor da matriz: " + str(matrix_min_value))

input('\nPrecione qualquer tecla para encerrar a aplicação.')
