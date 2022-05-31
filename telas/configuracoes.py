from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from tools.config import Settings

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '500')
Config.write()

paleta = {
    1:(0.145, 0.01, 0.333, 1), 
    2:(0.31, 0.21, 0.65, 1),
    3:(0.5, 0.36, 0.86, 1),
    4:(213/255, 0, 0, 1),
    5:(185/255, 0, 0, 1),
    6:(255, 81/255, 49/255, 1),
    7:(33/255, 33/255, 33/255, 1),
    8:(0, 0, 0, 1),
    9:(72/255, 72/255, 72/255, 1)
}

def text(string = 'Nome não definido', tipo=1):
    fontes = {
        1:'assets/fonte_principal.ttf',
        2:'assets/fonte_secundaria.ttf'
    }
    font_open = '[font='
    font_close = ']'
    font_end = '[/font]'
    return font_open+fontes[tipo]+font_close+str(string)+font_end

class BotaoPadrao(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markup = True
        self.size_hint = (None, None)
        self.width = 250
        self.height = 40
        self.background_normal = ''
        self.background_color = Settings().secundaria()

class LabelPadrao(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markup = True
        self.font_size = 18
        self.size_hint = (None, 1)
        self.width = 250

class Configuracoes(Screen):
    def __init__(self, fonte = 18, **kwargs):
        super().__init__(**kwargs)

        self.name = 'Configuracoes'

        self.padrao = 'Roxo'
        self.fonte = fonte

        self.draw()


    def draw(self):
        '''Desenha a interface
        '''
        self.box = FloatLayout()

        self.grid = GridLayout(
            cols = 2,
            rows = 4,
            row_force_default = True,
            pos_hint = {'x': 0.1, 'y': -0.2},
            row_default_height = 40,
            spacing = [0, 50]
        )

        self.labLoc = LabelPadrao(text = text('Nome da cidade: '))
        self.inpLoc = TextInput(
            halign = 'center',
            hint_text = Settings().localizacao(),
            hint_text_color = (0.9, 0.9, 0.9, 1),
            foreground_color = (12/255, 12/255, 12/255, 1),
            cursor_color = (12/255, 12/255, 12/255, 1),
            background_normal = '',
            background_color = Settings().terciaria(),
            font_size = self.fonte,
            multiline = False,
            size_hint = (None, 1),
            width = 250
        )

        self.labTem = LabelPadrao(text = text("Esquema de Cores: "))
        temas = ['Roxo', 'Vermelho', 'Escuro']
        self.dropTem = self.drop(temas)

        self.boxConfirmar = AnchorLayout(anchor_x='left', anchor_y ='center')
        self.confirmar = BotaoPadrao(on_release = self.capturar, text=Settings().text('Confirmar', 1))
        self.boxConfirmar.add_widget(self.confirmar)

        self.boxCancelar = AnchorLayout(anchor_x='left', anchor_y ='center')
        self.cancelar = BotaoPadrao(on_release = self.back, text=text('Cancelar'))
        self.boxCancelar.add_widget(self.cancelar)

        self.grid.add_widget(self.labLoc)
        self.grid.add_widget(self.inpLoc)
        self.grid.add_widget(self.labTem)
        self.grid.add_widget(self.dropTem)
        self.grid.add_widget(self.boxCancelar)
        self.grid.add_widget(self.boxConfirmar)

        self.box.add_widget(self.grid)

        self.add_widget(self.box)

    def back(self, button):
        ObjConfiguracoes.parent.current = "ClimaEventos"

    def capturar(self, dropFont):
            if(self.dropTem.text[33:-7] == 'Roxo'):
                primaria = paleta[1]
                secundaria = paleta[2]
                terciaria = paleta[3]
                self.padrao = 'Roxo'
            if(self.dropTem.text[33:-7] == 'Vermelho'):
                primaria = paleta[4]
                secundaria = paleta[5]
                terciaria = paleta[6]
                self.padrao = 'Vermelho'
            if(self.dropTem.text[33:-7] == 'Escuro'):
                primaria = paleta[7]
                secundaria = paleta[8]
                terciaria = paleta[9]
                self.padrao = 'Escuro'

            Settings().gravar(self.inpLoc.text, primaria, secundaria, terciaria)
            Settings().carregar()

            ObjConfiguracoes.parent.update()

            self.back(self.confirmar)

    def drop(self, botoes):
        dropdown = DropDown()

        for botao in botoes:
            btn = Button(
                markup = True,
                text = Settings().text(str(botao), 1),
                size_hint = (None, None),
                height = 40,
                font_size = self.fonte,
                width = 250,
                background_normal = '',
                background_color = Settings().secundaria()
            )

            btn.bind(on_release = lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        mainbutton = BotaoPadrao(text = Settings().text(self.padrao, 1))
        mainbutton.bind(on_release = lambda *args: dropdown.open(mainbutton))

        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, 'text', x))

        return mainbutton

ObjConfiguracoes = Configuracoes()