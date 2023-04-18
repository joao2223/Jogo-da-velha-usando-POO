'''Algumas engines para jogar TicTacToe'''

# ------------------------------------------------------------------------------
#
# engines do jogo.
#
# ------------------------------------------------------------------------------

import random
import copy
from board import Estadojogo, Jogodavelha

# --------------------------------------
#
# Escolha aleatoria simples.
#
# --------------------------------------


def lista_vazia(game):
    '''Gera uma lista de todos os espacos vazios no tabuleiro de jogo.'''

    # Encontre espaços vazios.
    options = [(i, j) for i in range(3) for j in range(3)
               if game.busca_espaco(i, j) == Estadojogo.EMPTY]
    return options


def mov_aleatorio(game):
    '''Calcula o movimento da máquina aleatoriamente.

    Escolhe aleatoriamente um espaco vazio. Presume que ha espacos vazios para escolher.'''

    # Retorna um dos espaços vazios.
    return random.choice(lista_vazia(game))


# --------------------------------------
#
# Cuidado com as linhas.
#
# --------------------------------------


def evita_perder(game):
    '''Calcule o movimento da maquina em busca de vitorias ou derrotas imediatas.

    Tenta encontrar uma vitoria. Caso contrario, tenta evitar uma vitoria para o humano.
    Caso contrario, escolha aleatoriamente.'''

    # Pega os espaços vazios.
    empty_cells = lista_vazia(game)

    # Se tem 9 espacos vazios, ainda estamos comecando. Basta escolher um espaco aleatorio.
    if len(empty_cells) == 9:
        return random.choice(empty_cells)

       # Cria uma copia de rascunho do jogo
    game_copy = copy.deepcopy(game) 

    # Tentar encontrar uma jogada vencedora.
    for r, c in empty_cells:
        # Definir o espaco vazio como maquina e verificar se isso da uma vitoria.
        game_copy.escolhe_espaco(r, c, Estadojogo.MACHINE)
        if (game_copy.has_finished() and
            game_copy.vencedor and
            game_copy.vencedor == Estadojogo.MACHINE):
            # Se for uma vitoria, devolva este espaco
            return r, c
        # Caso contrario, cancele o movimento falso e tente outro.
        game_copy.escolhe_espaco(r, c, Estadojogo.EMPTY)

    # Tenta encontrar um espaco que seja vencedor para o humano.
    # Mesma logica acima.
    for r, c in empty_cells:
        game_copy.escolhe_espaco(r, c, Estadojogo.humano)
        if (game_copy.has_finished() and
            game_copy.vencedor and
            game_copy.vencedor == Estadojogo.humano):
            return r, c
        game_copy.escolhe_espaco(r, c, Estadojogo.EMPTY)

    # Nenhum espaco para ganhar ou perder foi encontrado. Escolha aleatoriamente.
    return random.choice(empty_cells)
