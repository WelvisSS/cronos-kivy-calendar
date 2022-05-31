from  kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout 
from datetime import datetime
from tools.dataeventos.eventos import getdateevent, createevent
from tools.dataeventos.date import Date

class LayoutEventosDoDia(FloatLayout):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
                     
    def draw(self): 
            # teste = Date(21, 1, 2020)
            # createevent(teste, 'Nome Evento', 'Descrição Evento')
            a = getdateevent(Date().getDateNow())
            
            if a != None:
                a = a.split('-')
            else:
                a = ['Sem Eventos ',' ',' ']
            
            self.add_widget(Label(text=a[0], font_size=35, pos_hint={'x':0.25, 'y':0.4}))
            self.add_widget(Label(text=a[1], font_size=30, pos_hint={'x':0.25, 'y':0.25}))
            self.add_widget(Label(text=a[2], font_size=18, pos_hint={'x':0.25, 'y':0.0}))

    def update(self):           
        self.clear_widgets()
        self.draw()
        
