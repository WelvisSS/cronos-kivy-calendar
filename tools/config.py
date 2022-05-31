import os

class Settings():
    def __init__(self):
        super().__init__()
        self.opcoes = []

        if(os.path.isfile("assets\source\config.txt")):
            self.carregar()
        else:
            self.gravar("Ilhéus", (0.145, 0.01, 0.333, 1), (0.31, 0.21, 0.65, 1), (0.5, 0.36, 0.86, 1))
            self.carregar()

    def carregar(self):
        config = open("assets\source\config.txt", "r")
        for linha in config:
            self.opcoes.append(linha)
        

    def text(self, string = 'Nome não definido', tipo = 1):
        fontes = {
            1:'assets/fonte_principal.ttf',
            2:'assets/fonte_secundaria.ttf'
        }
        font_open = '[font='
        font_close = ']'
        font_end = '[/font]'
        return font_open + fontes[tipo] + font_close + str(string) + font_end

    def localizacao(self):
        return self.opcoes[0]

    def primaria(self):
        primaria = []
        aux = self.opcoes[1].replace('(', '').replace(')', '')
        primaria = aux.split(',')
        for i in range(len(primaria)):
            primaria[i] = float(primaria[i])

        return primaria

    def secundaria(self):
        secundaria = []
        aux = self.opcoes[2].replace('(', '').replace(')', '')
        secundaria = aux.split(',')
        for i in range(len(secundaria)):
            secundaria[i] = float(secundaria[i])
        return secundaria

    def terciaria(self):
        terciaria = []
        aux = self.opcoes[3].replace('(', '').replace(')', '')
        terciaria = aux.split(',')
        for i in range(len(terciaria)):
            terciaria[i] = float(terciaria[i])
        return terciaria

    def gravar(self, loc, primaria, secundaria, terciaria):
        config = open("assets\source\config.txt", "w")
        config.write(str(loc) + '\n')
        config.write(str(primaria) + '\n')
        config.write(str(secundaria) + '\n')
        config.write(str(terciaria) + '\n')