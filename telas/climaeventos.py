from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.core.window import Window
from tools.config import Settings 
from telas.auxclimaeventos.Clima import ObjLayoutClima 
from telas.auxclimaeventos.EventosDia import LayoutEventosDoDia

teste = LayoutEventosDoDia()
class Layout(FloatLayout):  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw()

    def draw(self):    
        
        self.add_widget(ObjLayoutClima)
        teste.update()
        self.add_widget(teste)
        
        self.add_widget(Button(text='Calen', background_color=Settings().primaria(), size_hint=[.1, .1], pos_hint={'x':.6, 'y':.06},
          on_release=self.telaCalendario))
        self.add_widget(Button(text='Config', background_color=Settings().primaria(), size_hint=[.1, .1], pos_hint={'x':.7, 'y':.06},
          on_release=self.telaConfiguracoes))
        self.add_widget(Button(text='Lista', background_color=Settings().primaria(), size_hint=[.1, .1], pos_hint={'x':.8, 'y':.06},
          on_release=self.telaListaEventos))

    def telaCalendario(self, button):
        ObjClimaEventos.parent.current = 'CriarEvento'
    def telaConfiguracoes(self, button):
        ObjClimaEventos.parent.current = 'Configuracoes'
    def telaListaEventos(self, button):
        ObjClimaEventos.parent.current = 'ListaEventos'

class ClimaEventos(Screen):  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'ClimaEventos'   
        self.Layout = Layout()
        self.add_widget(self.Layout)

    def update(self):           
        self.Layout.clear_widgets()
        self.Layout.draw()

ObjClimaEventos = ClimaEventos()