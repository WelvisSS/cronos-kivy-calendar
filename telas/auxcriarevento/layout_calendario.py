from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

import os
from tools.calendario_layer.gregorianus import CalendarioGregoriano

from tools.dataeventos.date import Date
from tools.dataeventos.eventos import hasevent, getdateevent

from tools.config import Settings

lista_do_mes_calendario = CalendarioGregoriano(1, 2020)
click_int = [Date().getDateNow().getDay(), Date().getDateNow().getMonth(), Date().getDateNow().getYear()]
click = ['Dia = '+str(click_int[0]), 'Mês = '+str(click_int[1]), 'Ano = '+str(click_int[2])]


class MostraEvento(Popup):
    def __init__(self, dia, mes, ano, **kwargs):
        super().__init__( **kwargs)
        self.dia = dia
        self.mes = mes
        self.ano = ano

        self.conteudo = getdateevent(Date(self.dia, self.mes, self.ano))

        self.background_color = (238/255, 238/255, 238/255, .3)
        self.title = str(self.conteudo.split('-')[0])+': '+str(self.conteudo.split('-')[1])
        self.size_hint = (None, None)
        self.height = 200
        self.width = 320

        self.botao_fechar = Button(
            size_hint = (None, None),
            width = 100,
            height = 60,
            markup= True,
            text=Settings().text('Fechar')
        )
        self.botao_fechar.bind(on_release=self.fecharPu)
        self.botao_tela_edicao = Button(
            size_hint = (None, None),
            width=200,
            height = 60,
            markup=True,
            text=Settings().text('Editar Eventos')
        )
        self.botao_tela_edicao.bind(on_release=self.editar_tela)

        # print('[   PopUp Aberto    ] String recebida : '+str(self.conteudo.split('-')[1]))
        self.bar_corp = BoxLayout(orientation='vertical')
        self.bar_button = BoxLayout(orientation='horizontal')

        self.bar_button.add_widget(self.botao_fechar)
        self.bar_button.add_widget(self.botao_tela_edicao)

        self.bar_corp.add_widget(Label(
            size_hint = (None, None),
            height = 60,
            width = self.width,
            markup=True,
            text = Settings().text(self.conteudo.split('-')[2]))
        )
        self.bar_corp.add_widget(self.bar_button)

        self.content = self.bar_corp
    def fecharPu(self, botao_fechar):
        self.dismiss()

    def editar_tela(self, botao_tela_edicao):
        corpo_geral.parent.parent.parent.current = 'ListaEventos'
        self.dismiss()


class nodoCalendario(BoxLayout):
    def __init__(self, dia, mes, ano, color_back=(37/255, 25/255, 85/255, 1), color_font = (1, 1, 1, 1), evento=0, **kwargs):
        super().__init__(**kwargs)
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.evento = evento

        self.botao = Button(markup=True, text=Settings().text(str(dia)))
        self.botao.background_color = color_back
        self.botao.background_normal = ''
        self.botao.color = color_font
        self.botao.bind(on_release=self.clicou)
        # self.botao.background_color = (79/255, 54/255, 165/255, 1)

        self.add_widget(self.botao)

    def clicou(self, botao):
        click[0] = 'Dia: '+str(self.dia)
        click[1] = 'Mês: '+str(self.mes)
        click[2] = 'Ano: '+str(self.ano)
        corpo_geral.atual_dia = self.dia
        corpo_geral.atual_mes = lista_do_mes_calendario.get_mes_int()
        corpo_geral.atual_ano = lista_do_mes_calendario.get_ano_int()
        click_int[0] = self.dia
        click_int[1] = lista_do_mes_calendario.get_mes_int()
        click_int[2] = lista_do_mes_calendario.get_ano_int()
        corpo_geral.parent.children[0].children[3].dia.text = Settings().text(click[0])
        corpo_geral.parent.children[0].children[3].mes.text = Settings().text(click[1])
        corpo_geral.parent.children[0].children[3].ano.text = Settings().text(click[2])
        # print(click)
        if self.evento==1:
            self.pop = MostraEvento(self.dia, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int())
            self.pop.open()


class FolhaCalendario(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 7
        self.rows = 7
        self.add_widget(Label(markup=True, text=Settings().text('Dom')))
        self.add_widget(Label(markup=True, text=Settings().text('Seg')))
        self.add_widget(Label(markup=True, text=Settings().text('Ter')))
        self.add_widget(Label(markup=True, text=Settings().text('Qua')))
        self.add_widget(Label(markup=True, text=Settings().text('Qui')))
        self.add_widget(Label(markup=True, text=Settings().text('Sex')))
        self.add_widget(Label(markup=True, text=Settings().text('Sab')))

        self.ant = 1
        self.atual = 0
        self.post = 0
        self.primo = 0

        for i in lista_do_mes_calendario.listar_mes():
            if i == 1:
                if self.primo < 2:
                    self.ant = 0
                    self.post = 0
                    self.atual = 1
                    self.primo += 1


            if self.primo >= 2:
                self.atual = 0
                self.ant = 0
                self.post = 1
            
            if self.ant == 1:
                '''Escreve a sobra do mes anterior
                '''
                lista_do_mes_calendario.anterior_mes()
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (79/255, 54/255, 165/255, 1)
                    )
                )
                lista_do_mes_calendario.proximo_mes()

            if self.atual == 1 and not(i == Date().getDateNow().getDay() and lista_do_mes_calendario.get_mes_int() == Date().getDateNow().getMonth() and lista_do_mes_calendario.get_ano_int() == Date().getDateNow().getYear() and self.atual ==1) and not(hasevent(Date(i, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int()))):
                '''Para dias normais
                '''
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (37/255, 25/255, 85/255, 1)
                    )
                )
                # print('há um evento em '+ str(i))
                if i == lista_do_mes_calendario.get_dias_mes() and self.atual==1:
                    self.primo += 1

            if self.post == 1:
                '''Escreve a parte do outro mes
                '''
                lista_do_mes_calendario.proximo_mes()
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (79/255, 54/255, 165/255, 1)
                    )
                )
                lista_do_mes_calendario.anterior_mes()

            if i == Date().getDateNow().getDay() and lista_do_mes_calendario.get_mes_int() == Date().getDateNow().getMonth() and lista_do_mes_calendario.get_ano_int() == Date().getDateNow().getYear() and self.atual ==1 and not(hasevent(Date(i, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int()))):
                '''Define o dia de hoje
                '''
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (238/255, 238/255, 238/255, 1),
                    color_font = (0, 0, 0, 1)
                    )
                )
                if i == lista_do_mes_calendario.get_dias_mes() and self.atual==1:
                    self.primo += 1

            if self.atual == 1 and hasevent(Date(i, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int())) and not(i == Date().getDateNow().getDay() and lista_do_mes_calendario.get_mes_int() == Date().getDateNow().getMonth() and lista_do_mes_calendario.get_ano_int() == Date().getDateNow().getYear()):
                '''Define se há evento
                '''
                # print('há um evento em '+ str(i))
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (191/255, 54/255, 12/255, 1),
                    evento=1
                    # color_font = (0, 0, 0, 1)
                    )
                )

            if self.atual == 1 and hasevent(Date(i, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int())) and i == Date().getDateNow().getDay() and lista_do_mes_calendario.get_mes_int() == Date().getDateNow().getMonth() and lista_do_mes_calendario.get_ano_int() == Date().getDateNow().getYear():
                '''Define se há um evento hoje
                '''
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (0/255, 61/255, 51/255, 1),
                    evento=1
                    # color_font = (0, 0, 0, 1)
                    )
                )

    def atualiza_folha(self):
        self.primo = 0
        self.ant = 1
        self.atual = 0
        self.post = 0
        self.primo = 0
        self.clear_widgets()
        self.add_widget(Label(markup=True, text=Settings().text('Dom')))
        self.add_widget(Label(markup=True, text=Settings().text('Seg')))
        self.add_widget(Label(markup=True, text=Settings().text('Ter')))
        self.add_widget(Label(markup=True, text=Settings().text('Qua')))
        self.add_widget(Label(markup=True, text=Settings().text('Qui')))
        self.add_widget(Label(markup=True, text=Settings().text('Sex')))
        self.add_widget(Label(markup=True, text=Settings().text('Sab')))

        for i in lista_do_mes_calendario.listar_mes():
            if i == 1:
                if self.primo < 2:
                    self.ant = 0
                    self.post = 0
                    self.atual = 1
                    self.primo += 1


            if self.primo >= 2:
                self.atual = 0
                self.ant = 0
                self.post = 1
            
            if self.ant == 1:
                lista_do_mes_calendario.anterior_mes()
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (79/255, 54/255, 165/255, 1)
                    )
                )
                lista_do_mes_calendario.proximo_mes()

            if self.atual == 1 and not(i == Date().getDateNow().getDay() and lista_do_mes_calendario.get_mes_int() == Date().getDateNow().getMonth() and lista_do_mes_calendario.get_ano_int() == Date().getDateNow().getYear() and self.atual ==1) and not(hasevent(Date(i, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int()))):
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (37/255, 25/255, 85/255, 1)
                    )
                )
                # print('há um evento em '+ str(i))
                if i == lista_do_mes_calendario.get_dias_mes() and self.atual==1:
                    self.primo += 1

            if self.post == 1:
                lista_do_mes_calendario.proximo_mes()
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (79/255, 54/255, 165/255, 1)
                    )
                )
                lista_do_mes_calendario.anterior_mes()

            if i == Date().getDateNow().getDay() and lista_do_mes_calendario.get_mes_int() == Date().getDateNow().getMonth() and lista_do_mes_calendario.get_ano_int() == Date().getDateNow().getYear() and self.atual ==1 and not(hasevent(Date(i, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int()))):
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (238/255, 238/255, 238/255, 1),
                    color_font = (0, 0, 0, 1)
                    )
                )
                if i == lista_do_mes_calendario.get_dias_mes() and self.atual==1:
                    self.primo += 1

            if self.atual == 1 and hasevent(Date(i, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int())):
                # print('há um evento em '+ str(i))
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (191/255, 54/255, 12/255, 1),
                    # color_font = (0, 0, 0, 1)
                    )
                )
            if self.atual == 1 and hasevent(Date(i, lista_do_mes_calendario.get_mes_int(), lista_do_mes_calendario.get_ano_int())) and i == Date().getDateNow().getDay() and lista_do_mes_calendario.get_mes_int() == Date().getDateNow().getMonth() and lista_do_mes_calendario.get_ano_int() == Date().getDateNow().getYear():
                '''Define se há um evento hoje
                '''
                self.add_widget(nodoCalendario(
                    dia = i,
                    mes = lista_do_mes_calendario.get_mes_str(),
                    ano = lista_do_mes_calendario.get_ano_str(),
                    color_back = (0/255, 61/255, 51/255, 1),
                    evento=1
                    # color_font = (0, 0, 0, 1)
                    )
                )

folha_calendario = FolhaCalendario()

class AreaAno(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.halign = 'center'
        self.size_hint_y = None
        self.height = 40
        self.name = 'assets/fonte_principal'
        self.font_size = 23
        self.foreground_color = (238/255, 238/255, 238/255, 1)
        self.text = lista_do_mes_calendario.get_ano_str()
        self.background_color = (129/255, 93/255, 220/255, 1)
        self.cursor_color = (129/255, 93/255, 220/255, 1)
    def on_focus(self, area_ano, value):
        if value:
            self.text = ''
        else:
            if self.text == '' or not self.text.isnumeric():
                lista_do_mes_calendario.set_ano(lista_do_mes_calendario.get_ano_int())
                self.text = lista_do_mes_calendario.get_ano_str()
            else:
                lista_do_mes_calendario.set_ano(int(self.text))
                lista_do_mes_calendario.set_mes(1)
                folha_calendario.atualiza_folha()
                info_mes.att()


class BotaoProximo(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # lista_do_mes_calendario.proximo_mes()
        self.size_hint_y = None
        self.height = 40
        self.markup = True
        self.font_size = 17
        self.text = Settings().text('Prox')

class BotaoAnterior(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # lista_do_mes_calendario.anterior_mes()
        self.size_hint_y = None
        self.height = 40
        self.font_size = 17
        self.markup = True
        self.text = Settings().text('Ant')


class InfoMes(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 70
        self.markup = True
        self.font_size = 23
        self.text = Settings().text(lista_do_mes_calendario.get_mes_str())
    def att(self):
        self.text = Settings().text(lista_do_mes_calendario.get_mes_str())
info_mes = InfoMes()
    
class BarraSuperior(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50

        self.bott_prox = BotaoProximo()
        self.bott_prox.background_color = (37/255, 25/255, 85/255, 1)
        self.area_ano = AreaAno()
        self.bott_ant = BotaoAnterior()
        self.bott_ant.background_color = (37/255, 25/255, 85/255, 1)

        self.add_widget(self.bott_ant)
        self.add_widget(self.area_ano)
        self.add_widget(self.bott_prox)
        

class CorpoCalendario(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.atual_dia = click_int[0]
        self.atual_mes = lista_do_mes_calendario.get_mes_int()
        self.atual_ano = lista_do_mes_calendario.get_ano_int()

        self.top_bar = BarraSuperior()
        self.top_bar.bott_ant.bind(on_release=self.voltar_mes)
        self.top_bar.bott_prox.bind(on_release=self.avancar_mes)

        self.add_widget(self.top_bar)
        self.add_widget(info_mes)
        self.add_widget(folha_calendario)

    def voltar_mes(self, bott_ant):
        lista_do_mes_calendario.anterior_mes()
        info_mes.text = lista_do_mes_calendario.get_mes_str()
        self.top_bar.area_ano.text = lista_do_mes_calendario.get_ano_str()
        folha_calendario.atualiza_folha()

    def avancar_mes(self, bott_prox):
        lista_do_mes_calendario.proximo_mes()
        info_mes.att()
        self.top_bar.area_ano.text = lista_do_mes_calendario.get_ano_str()
        folha_calendario.atualiza_folha()

corpo_geral = CorpoCalendario()