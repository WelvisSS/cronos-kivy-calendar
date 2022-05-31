from kivy.uix.screenmanager import ScreenManager
from telas.listaeventos import Lista_Eventos
from telas.climaeventos import ObjClimaEventos
from telas.criarevento import ObjCriarEvento
from telas.configuracoes import ObjConfiguracoes

#Fabiano
#   name = ListaEventos
#Welvis
#   ClimaEventos
#Thiago
#    name = CriarEvento
#Breno
#    name = Configuracoes

class adm(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Lista_Eventos)
        self.add_widget(ObjClimaEventos)
        self.add_widget(ObjCriarEvento)
        self.add_widget(ObjConfiguracoes)
        self.current = 'ClimaEventos'

    def update(self):
        ObjConfiguracoes.draw()
        Lista_Eventos.update()
        ObjCriarEvento.update()
        ObjClimaEventos.update()

Adm = adm()