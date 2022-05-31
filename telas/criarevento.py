from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.label import Label
from kivy.uix.button import Button

from telas.auxcriarevento.layout_calendario import corpo_geral
from telas.auxcriarevento.formulario import ObjFormulario
from tools.config import Settings

#texto settings.text(texto)
#paleta settings.primaria

class TopBar(AnchorLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'right'
        self.anchor_y = 'top'

        self.home = Button(markup=True, text=Settings().text(string='Home'))
        self.home.size_hint = (None, None)
        self.home.width = 60
        self.home.height = 30
        self.home.background_color = (37/255, 25/255, 85/255, 1)
        self.home.bind(on_release=self.casa)
        self.add_widget(self.home)

    def casa(self, home):
        ObjCriarEvento.parent.current = 'ClimaEventos'

class Corpo(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 50

        self.add_widget(corpo_geral) #1
        # self.add_widget(Label(text='Área De Criação do evento'))
        self.add_widget(ObjFormulario) #0

class CriarEvento(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'CriarEvento'
        self.barra = TopBar()
        self.corpo = Corpo()
        self.add_widget(self.barra)
        self.add_widget(self.corpo)
    def update(self):
        self.corpo.children[1].children[0].atualiza_folha()
        self.clear_widgets()
        self.add_widget(self.barra)
        self.add_widget(self.corpo)


ObjCriarEvento = CriarEvento()