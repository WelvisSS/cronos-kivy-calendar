from kivy.uix.boxlayout import BoxLayout

from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from tools.dataeventos.eventos import createevent
from tools.dataeventos.date import Date

from tools.config import Settings

class ValidaEvento(Popup):
    def __init__(self, estado = 0, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.width = 600
        self.height = 200
        self.background_color = (238/255, 238/255, 238/255, .5)
        self.corpo = BoxLayout(orientation='vertical')
        if estado == 0:
            self.title = 'Erro'
            self.corpo.add_widget(Label(
                markup=True,
                halign='center',
                text=Settings().text('O evento não foi criado porque os dois campos não foram preenchidos')
                )
            )
            self.corpo.add_widget(Button(
                halign='center',
                markup=True,
                text=Settings().text('Voltar para remarcar evento'),
                on_release = self.dismiss
                )
            )
        else:
            self.title = 'Confirmação'
            self.corpo.add_widget(Label(
                halign='center',
                markup=True,
                text=Settings().text('Evento criado')
                )
            )
            self.corpo.add_widget(Button(
                markup=True,
                text=Settings().text('Ok'),
                halign = 'center',
                on_release = self.dismiss
                )
            )
        self.content = self.corpo

class Data(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.dia = Label(font_size = 17, markup=True, text=Settings().text('Dia: '+str(Date().getDateNow().getDay())))
        self.mes = Label(font_size = 17, markup=True, text=Settings().text('Mes: '+str(Date().getDateNow().getMonth())))
        self.ano = Label(font_size = 17, markup=True, text=Settings().text('Ano: '+str(Date().getDateNow().getYear())))

        self.add_widget(self.dia) #2
        self.add_widget(self.mes) #1
        self.add_widget(self.ano) #0

class Title(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 60

        self.input_title = TextInput(
            font_name = 'assets/fonte_principal',
            font_size = 17,
            background_color = (238, 238, 238, 1),
            cursor_color = (238, 238, 238, 1),
            multiline = False, 
            size_hint = (None, None),
            height = 60,
            width = 350,
        )

        self.add_widget(Label(
            markup=True, 
            text=Settings().text('Título: '),
            size_hint = (None, None),
            height = 60,
            width = 90
        )
        )
        self.add_widget(self.input_title)

class Descricao(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.input_descricao = TextInput(
            font_name = 'assets/fonte_principal',
            font_size = 17,
            background_color = (238, 238, 238, 1),
            cursor_color = (238, 238, 238, 1),
            multiline = False, 
            size_hint = (None, None),
            height = 60,
            width = 350,
        )

        self.add_widget(Label(
            markup=True, 
            text=Settings().text('Descrição: '),
            size_hint = (None, None),
            height = 60,
            width = 100
            )
        )
        self.add_widget(self.input_descricao)

class Formulario(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 30
        self.data = Data()
        self.titulo = Title()
        self.descricao = Descricao()
        
        self.criar = Button(markup=True, text=Settings().text('Adicionar Evento'))
        self.criar.size_hint_y = None
        self.criar.height = 50
        self.criar.background_color = (37/255, 25/255, 85/255, 1)
        self.criar.bind(on_release=self.criacao)

        self.add_widget(self.data) #3
        self.add_widget(self.titulo) #2
        self.add_widget(self.descricao) #1
        self.add_widget(self.criar) #0
    
    def criacao(self, criar):
        if self.descricao.input_descricao.text != '' and self.titulo.input_title.text != '':
            createevent(
                Date(
                    ObjFormulario.parent.children[1].atual_dia,
                    ObjFormulario.parent.children[1].atual_mes,
                    ObjFormulario.parent.children[1].atual_ano
                ),
                self.titulo.input_title.text,
                self.descricao.input_descricao.text
            )
            self.descricao.input_descricao.text = ''
            self.titulo.input_title.text = ''
            ValidaEvento(estado=1).open()
        else:
            ValidaEvento().open()
        ObjFormulario.parent.children[1].children[0].atualiza_folha()
        ObjFormulario.parent.parent.parent.update()


ObjFormulario = Formulario() #preciso acessar isso