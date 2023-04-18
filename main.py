import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

from board import Estadojogo, Jogodavelha
from engines import *


class Botaodojogo(ttk.Button
                  ):  #classe que representa o botao que inicia o jogo
    def __init__(self, parent, r, c, img):
        def botao_pressionado():
            parent.escolhe_espaco(r, c, Estadojogo.humano)

        super().__init__(parent, image=img, command=botao_pressionado)
        self.grid(row=r, column=c)


class Quadrocombotoes(ttk.Frame
                      ):  # classe que representa os 9 botoes do jogo da velha
    def __init__(self, parent, estado):
        super().__init__(parent)
        self._parent = parent
        self._estado = estado
        self._imgs = [
            tk.PhotoImage(file='images/' + f)
            for f in ['e.png', 'o.png', 'xi.png']
        ]

        self._botoes = [[
            Botaodojogo(self, r, c, self._imgs[estado.busca_espaco(r, c)])
            for c in range(3)
        ] for r in range(3)]

    def escolhe_espaco(self, r, c, value):
        tabuleiro = self._estado
        if tabuleiro.busca_espaco(r, c) == Estadojogo.EMPTY:
            tabuleiro.escolhe_espaco(r, c, value)
            self._botoes[r][c].config(image=self._imgs[value])
            if tabuleiro.has_finished():
                self._parent.game_over()
            elif value == Estadojogo.humano:
                self._parent.movimento_do_computador()


class TTTplaca(tk.Toplevel):  #tela principal que comeca o jogo
    def __init__(self, parent, o_oponente, vez_computador):
        super().__init__()  #init do Toplevel
        self._parent = parent
        self._oponente = o_oponente

        parent.desabilita_botoes()  #desabilita os botoes

        self._estado = Jogodavelha()
        if vez_computador:  #verifica se é a vez do computador
            r, c = o_oponente(self._estado)
            self._estado.escolhe_espaco(r, c, Estadojogo.MACHINE)

        self.focus()  #faz a janela receber as entradas

        self.title('O jogo começou!')
        self.resizable(width=False,
                       height=False)  #nao nmuda o tamanho da janela

        self._w_var = tk.IntVar()  # Variavel para esperar o final do jogo
        self._w_var.set(0)

        # Criar os botões do tabuleiro
        self._tabuleiro = Quadrocombotoes(self, self._estado)
        self._tabuleiro.pack()

        # Registra o evento de fechamento de janela.
        self.protocol('WM_DELETE_WINDOW', lambda: self._w_var.set(1))

    def play(self):
        # aguarda o botao sair ou o evento de fechamento da janela.
        self.wait_variable(self._w_var)
        self._parent.habilita_botoes()
        self.destroy()

    def movimento_do_computador(self):  #funcao para o movimento do computador
        r, c = self._oponente(self._estado)
        self._tabuleiro.escolhe_espaco(r, c, Estadojogo.MACHINE)

    def game_over(self):  #metodo chamado quando o jogo termina
        if self._estado.vencedor:
            win = 'jogador' if self._estado.vencedor == Estadojogo.humano else 'computador'
            mess = f'O vencedor é o {win}!'
        else:
            mess = 'Empate!'
        tkinter.messagebox.showinfo(parent=self,
                                    title='Fim de jogo!',
                                    message=mess)
        self._w_var.set(1)


# --------------------------------------
#
# A UI de configuração.
#
# --------------------------------------


class JogodavelhaUI(tk.Tk):  #classe que inicia o jogo
    def __init__(self):
        super().__init__()  #inicia o tk.Tk

        self.vez_computador = None
        self._identidade_oponente = None

        self.title('Jogo da velha')  #titulo da janela
        self.iconphoto(True, tk.PhotoImage(file='ttt.png'))
        self.resizable(width=False, height=False)  #janela de tamanho fixo

        label = ttk.Label(
            self, text='Escolha as opções'
        )  #janela que inicia o jogo, pedindo para escolher as opções.

        label.grid(row=0, column=0, columnspan=2, padx=20,
                   pady=10)  #posicionar os botoes na tela

        # widgets de escolha do oponente.
        opponents = ttk.LabelFrame(self, text='Oponente')
        opponents.grid(row=1, column=0, padx=20, pady=0, ipady=5, sticky=tk.N)

        self._identidade_oponente = tk.IntVar()
        self._identidade_oponente.set(0)

        ttk.Radiobutton(opponents,
                        text='Einstein',
                        variable=self._identidade_oponente,
                        value=0).pack(padx=10, anchor=tk.W)
        ttk.Radiobutton(opponents,
                        text='Spock',
                        variable=self._identidade_oponente,
                        value=1).pack(padx=10, anchor=tk.W)

        # Widgets de escolha do jogador inicial.
        starts = ttk.LabelFrame(self, text='Quem começa?')
        starts.grid(row=1, column=1, padx=20, pady=0, ipady=5, sticky=tk.N)

        self.vez_computador = tk.BooleanVar()
        self.vez_computador.set(True)

        #separando os dois casos, usando Radiobutton
        ttk.Radiobutton(starts,
                        text='Computador',
                        variable=self.vez_computador,
                        value=True).pack(padx=10, anchor=tk.W)
        ttk.Radiobutton(starts,
                        text='Humano',
                        variable=self.vez_computador,
                        value=False).pack(padx=10, anchor=tk.W)

        # Botoes de controle do jogo.
        self._quit = ttk.Button(self, text='Sair',
                                command=self.destroy)  #fecha a janela
        self._quit.grid(row=2, column=0, padx=20, pady=10)

        self._play = ttk.Button(
            self, text='Jogar', command=lambda: self.play_game(
            ))  #inicia o jogo, usa a funcao play_game, declarada mais abaixo.
        self._play.grid(row=2, column=1, padx=20, pady=10)

    def desabilita_botoes(self):
        self._quit.config(state=tk.DISABLED)
        self._play.config(state=tk.DISABLED)

    def habilita_botoes(self):
        self._quit.config(state=tk.NORMAL)
        self._play.config(state=tk.NORMAL)

    def play_game(self):  #funcao que comeca uma tela de jogo
        opponents = [mov_aleatorio, evita_perder]
        o_oponente = opponents[self._identidade_oponente.get(
        )]  #escolhe o oponente correspondente.
        vez_computador = self.vez_computador.get()  #verifica quem joga
        game_win = TTTplaca(self, o_oponente,
                            vez_computador)  #cria uma nova janela
        game_win.play()  #metodo que inicia o jogo

    def run(self):  #metodo para rodar o jogo
        self.mainloop(
        )  #loop principal do tk.Tk, espera o usuario ecolher o que fazer


if __name__ == '__main__':
    ttt = JogodavelhaUI()
    ttt.run()
