import kivy
from kivy.config import Config
kivy.config.Config.set('graphics','resizable', False)
from kivy.app import App
from kivy.core.window import Window
from adm_telas import Adm
from tools.dataeventos.eventos import createevent
from tools.dataeventos.date import Date

class Aplicativo(App):
    def build(self):
        self.title = 'Cronos'
        Window.size = (800, 500)
        Window.clearcolor = (37/255, 25/255, 85/255, 1)
        return Adm

Aplicativo().run()