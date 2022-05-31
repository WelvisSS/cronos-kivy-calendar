'''Essa é a classe que gera os dados e ferramentas para o aplicativo poder gerar a interface
'''
from tools.calendario_layer.validador import valida_mes, valida_ano

calendario_meses_dias = {
    0:0,
    1:3,
    2:3, #isso é 0 ou 1
    3:6,
    4:8,
    5:11,
    6:13,
    7:16,
    8:19,
    9:21,
    10:24,
    11:26,
    12:3,
}

calendario_meses_dias_string = {
    1:'Janeiro',
    2:'Fevereiro',
    3:'Março',
    4:'Abril',
    5:'Maio',
    6:'Junho',
    7:'Julho',
    8:'Agosto',
    9:'Setembro',
    10:'Outubro',
    11:'Novembro',
    12:'Dezembro'
}

calendario_meses_dias_int = {
    0:31,
    1:31,
    2:28,
    3:31,
    4:30,
    5:31,
    6:30,
    7:31,
    8:31,
    9:30,
    10:31,
    11:30,
    12:31
}

dias_da_semana = {
    0:'Terça',
    1:'Quarta',
    2:'Quinta',
    3:'Sexta',
    4:'Sábado',
    5:'Domingo',
    6:'Segunda',
}

contador_dia = {
    5:0,
    6:1,
    0:2,
    1:3,
    2:4,
    3:5,
    4:6
}

class CalendarioGregoriano(object):
    '''O formato padrão disposto nos parâmetros é CalendarioGregoriano(MM, AAAA) em tipo inteiro
    e a data padrão 1/1/1583 se baseia em um ano depois da atualização mais recente do calendário que usamos atualmente
    '''
    def __init__(self, mes=1, ano=1583):
        self.__base_ano = 1901
        if valida_ano(ano):
            self.__ano = ano
        else:
            self.__ano = self.__base_ano
        
        if valida_mes(mes):
            self.__mes = mes
        else:
            self.__mes = 1


    def verifica_bissexto(self, ano=0):
        '''Retorna True se o ano for bissexto ou False se o ano não o for.
        Para usar o ano atual selecionado na declaração do objeto dessa classe basta não digitar parâmetros ou igualar o parâmetro ano a 0

        Ex: CalendarioGregoriano.verifica_bissexto()

        Obs: Use sempre anos estritamente maiores que 1582
        '''
        if ano == 0:
            ano = self.__ano
        
        if ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0:
            return True
        else:
            return False


    def janos_primeiro(self):
        '''Retorna um número equivalente ao dia da semana da primeira data de cada ano (1/1)
        '''
        return (365*(self.__ano - self.__base_ano) + int((self.__ano - self.__base_ano)/4)) % 7

    def mes_primeiro(self, mes=0):
        '''Retorna o dia da semana referente ao primeiro primeiro dia de um mês específico
        '''
        if mes != 0:
            self.__mes = mes
            
        if mes == 1 or self.__mes==1:
            return self.janos_primeiro()
        elif self.verifica_bissexto() and self.__mes != 2:
            return (self.janos_primeiro() + calendario_meses_dias[self.__mes - 1] + 1) % 7
        else:
            return (self.janos_primeiro() + calendario_meses_dias[self.__mes - 1]) % 7


    def listar_mes(self):
        '''Mostra lista do mes atual com entrada e saída
        '''
        self.__tam = 42
        self.__lista_do_mes = []



        if self.verifica_bissexto() and self.__mes == 2:
            for i in range(1, calendario_meses_dias_int[self.__mes]+2):
                self.__lista_do_mes.append(i)
        else:
            for i in range(1, calendario_meses_dias_int[self.__mes]+1):
                self.__lista_do_mes.append(i)

        # self.__lista_entrada = calendario_meses_dias_int[self.__mes - 1] - contador_dia[self.mes_primeiro()] + 1
        self.__lista_entrada = []
        for i in range(calendario_meses_dias_int[self.__mes - 1] - contador_dia[self.mes_primeiro()] + 1, calendario_meses_dias_int[self.__mes-1]+1):
            self.__lista_entrada.append(i)

        if self.verifica_bissexto() and self.__mes == 3:
            self.__lista_entrada.append(29)

        self.lista_saida = []
        for i in range(1, self.__tam - calendario_meses_dias_int[self.__mes]):
            self.lista_saida.append(i)

        self.lista_completa = []
        self.lista_completa.extend(self.__lista_entrada)
        self.lista_completa.extend(self.__lista_do_mes)
        self.lista_completa.extend(self.lista_saida)

        return self.lista_completa[:42]



    '''As Próximas funções são referentes a funcionalidades que podem ser utilizadas pelo usuario
    '''

    def get_dias_mes(self):
        '''Retorna a quantidade de dias de um mes
        '''
        return calendario_meses_dias_int[self.__mes]

    def get_ano_int(self):
        '''Retorna o ano atual instanciado no objeto dessa classe na forma de um inteiro
        '''
        return self.__ano

    def get_mes_int(self):
        '''Retorna o mês atual instanciado no objeto dessa classe na forma de um inteiro
        '''
        return self.__mes

    def get_mes_str(self):
        '''Retorna o mês atual instanciado no objeto dessa classe
        '''
        return calendario_meses_dias_string[self.__mes]

    def get_ano_str(self):
        '''Retorna o ano atual instanciado no objeto dessa classe na forma de uma string
        '''
        return str(self.__ano)

    def proximo_mes(self):
        '''Retorna o próximo mes. Se passar do mês 12 o ano será alterado
        '''
        if self.__mes == 12:
            self.__ano += 1
            self.__mes = 1
            return self.__mes
        else:
            self.__mes += 1
            return self.__mes

    def proximo_ano(self):
        '''Vai para o próximo ano
        '''
        return self.__ano+1
        
    def anterior_mes(self):
        '''Retorna o próximo mes. Se passar do mês 12 o ano será alterado
        '''
        if self.__mes == 1:
            self.__ano -= 1
            self.__mes = 12
            return self.__mes
        else:
            self.__mes -= 1
            return self.__mes

    def anterior_ano(self):
        '''Vai para o próximo ano
        '''
        return self.__ano-1

    def set_ano(self, ano):
        if valida_ano(ano):
            self.__ano = ano
        else:
            self.__ano = self.__base_ano

    def set_mes(self, mes):
        if valida_mes(mes):
            self.__mes = mes
        else:
            self.__mes = 1

    def __str__(self):
        if self.verifica_bissexto():
            return 'ano: '+str(self.__ano)+'(bissexto):\n\tmês: '+calendario_meses_dias_string[self.__mes]+'. Dia da semana: '+dias_da_semana[self.mes_primeiro()]
        else:
            return 'ano: '+str(self.__ano)+'(não bissexto):\n\tmês: '+calendario_meses_dias_string[self.__mes]+'. Dia da semana: '+dias_da_semana[self.mes_primeiro()]
            