from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from tools.dataeventos.eventos import createevent, deleteevent, listevents, deleteall
from tools.dataeventos.date import Date
from tools.config import Settings

class OnListEvent(GridLayout):
    neventos = 0

    def __init__(self, date, event, description, screen, **kwargs):
        super().__init__(**kwargs)
        self.cols=5
        OnListEvent.neventos += 1

        # Atributos de cada evento
        self.__title = str(event)
        self.__description = str(description)
        self.__date = date
        self.__screen = screen

        # Widgets do grid
        self.numberevent = Label(text=Settings().text(str(OnListEvent.neventos)) + '-', size_hint=(0.15, 1), markup=True)
        self.eventlabel = Label(text=Settings().text(event + ' - ' + str(date)), markup=True)
        self.delbutton = Button(text=Settings().text('Del.'), size_hint=(0.15, 1), on_release=self.delete, markup=True, background_color=Settings().secundaria(), background_normal='')
        self.editbutton = Button(text=Settings().text('Edit'), size_hint=(0.15, 1), on_release=self.activate, markup=True, background_color=Settings().secundaria(), background_normal='') 

        self.add_widget(self.numberevent)
        self.add_widget(self.eventlabel)
        self.add_widget(self.delbutton)
        self.add_widget(self.editbutton)

    def delete(self, button):
        ''' Deleta o evento relacionado ao botão da lista '''
        deleteevent(self.__date)
        OnListEvent.neventos=0
        Lista_Eventos.detailsgrid.applybutton.disabled=True
        Lista_Eventos.parent.update()

    def activate(self, button):
        ''' Torna os dados relacionados ao botão o evento ativo do grid de edição '''
        DetailsGrid.activeevent = self
        self.__screen.update()

    def getDate(self):
        return self.__date

    def getDescription(self):
        return self.__description

    def getTitle(self):
        return self.__title


# Classe do painel direito
class DetailsGrid(GridLayout):
    activeevent = OnListEvent(Date(), ' ', ' ', screen=None)
    def __init__(self, screen,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.spacing = 5
        self.screen = screen

        # Area superior
        self.selectedeventlabel = Button(text=Settings().text('Evento Selecionado'), size_hint=(1, 0.1), markup=True, background_color=Settings().secundaria(), background_normal='')

        # Area do titulo do evento
        self.titlelabel = Label(text=Settings().text('Titulo do evento'), size_hint=(1, .20), markup=True)
        self.title = TextInput(text=DetailsGrid.activeevent.getTitle().strip(), size_hint=(1, 0.10), multiline=False, font_name='assets/fonte_principal')
        
        # Area da descrição do evento
        self.descriptionlabel = Label(text=Settings().text('Descrição do evento'), size_hint=(1, .20), markup=True)
        self.description = TextInput(text=DetailsGrid.activeevent.getDescription().strip(), multiline=False, halign='auto', size_hint=(1, .10), font_name='assets/fonte_principal')
        
        # Area da data do evento
        self.datelabel = Label(text=Settings().text('Data do evento (DD/MM/AAAA)'), size_hint=(1, .20), markup=True)
        self.day = TextInput(text=str(DetailsGrid.activeevent.getDate().getDay()).strip(), multiline=False, font_name='assets/fonte_principal', input_filter='int')
        self.month = TextInput(text=str(DetailsGrid.activeevent.getDate().getMonth()).strip(), multiline=False, font_name='assets/fonte_principal', input_filter='int')
        self.year = TextInput(text=str(DetailsGrid.activeevent.getDate().getYear()).strip(), multiline=False, font_name='assets/fonte_principal', input_filter='int')
        self.dategrid = GridLayout(rows=1, size_hint_y=.1, spacing=5)
        self.dategrid.add_widget(self.day)
        self.dategrid.add_widget(self.month)
        self.dategrid.add_widget(self.year)
        
        # Botão inferior de aplicar alterações
        self.applybutton = Button(text=Settings().text('Aplicar'), size_hint=(1, 0.1), on_release=self.applyedit, markup=True, background_color=Settings().secundaria(), background_normal='')
        if len(listevents()) == 0 or (DetailsGrid.activeevent.getDate().getDay() == Date().getDay() and DetailsGrid.activeevent.getDate().getMonth() == Date().getMonth() 
                                        and DetailsGrid.activeevent.getDate().getYear() == Date().getYear() and DetailsGrid.activeevent.getDescription() == ' '
                                        and DetailsGrid.activeevent.getTitle() == ' '):
            self.applybutton.disabled=True

        # Adicionando todos os widgets
        self.add_widget(self.selectedeventlabel)
        self.add_widget(self.titlelabel)
        self.add_widget(self.title)
        self.add_widget(self.descriptionlabel)
        self.add_widget(self.description)
        self.add_widget(self.datelabel)
        self.add_widget(self.dategrid)
        self.add_widget(self.applybutton)
        
    def applyedit(self, button):
        '''Aplica as edições ao arquivo '''
            
        if self.day.text == '' or self.month.text == '' or self.year.text == '' or self.description.text == '' or self.title.text == '':
            errorpopup = Popup(title='Campo vazio', content=Label(text=Settings().text('Insira os dados corretamente'), markup=True), size_hint=(None, None), size=(250, 150))
            errorpopup.open()
            
        elif Date().verifyDate(int(self.day.text), int(self.month.text), int(self.year.text)):
            deleteevent(DetailsGrid.activeevent.getDate())
            DetailsGrid.activeevent = OnListEvent(Date(int(self.day.text), int(self.month.text), int(self.year.text)), self.title.text.strip(), self.description.text.strip(), screen=Lista_Eventos)

            if self.description.text != '' and self.title.text != '':
                createevent(Date(int(self.day.text), int(self.month.text), int(self.year.text)), self.title.text.strip(), self.description.text.strip())

            OnListEvent.neventos = 0
            Lista_Eventos.parent.update()
        else:
            errorpopup = Popup(title='Data invalida', content=Label(text=Settings().text('Insira uma data válida'), markup=True), size_hint=(None, None), size=(250, 150))
            errorpopup.open()

    def disapleapply(self):
        ''' Desabilita o botão de aplicar '''
        self.applybutton.disabled=True

    def enableapply(self):
        ''' Habilita o botão de aplicar '''
        self.applybutton.disabled=False

# Classe do painel esquerdo
class ListGrid(GridLayout):
    def __init__(self, screen,**kwargs):
        super().__init__(**kwargs)
        OnListEvent.neventos = 0
        self.cols = 1
        self.size_hint_y = None
        self.spacing = 5
        self.screen = screen
        self.bind(minimum_height=self.setter('height'))
        
        for event in listevents():
            eventsplit = event.split('-')
            datesplit = eventsplit[1].split('/')
            self.add_widget(OnListEvent(height=30, size_hint_y=None, spacing=5,date=Date(int(datesplit[0]), int(datesplit[1]), int(datesplit[2])),
                                            event=eventsplit[0], description=eventsplit[2], screen=self.screen))

        if len(listevents()) == 0:
            self.add_widget(Label(text=Settings().text('Sem eventos'), markup=True))
        

class ListaEventos(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.draw()
        self.name = 'ListaEventos'

    def draw(self):
        # Widgets do lado esquerdo
        self.scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.scroll.add_widget(ListGrid(screen=self))
        self.backbutton = Button(text=Settings().text('<-'), size_hint_x=.2,on_release=self.backtohome, markup=True, background_color=Settings().secundaria(), background_normal='')
        self.updatebutton = Button(text=Settings().text('Atualizar'), on_release=self.update, markup=True, background_color=Settings().secundaria(), background_normal='')
        self.topbuttonsgrid = GridLayout(rows=1, size_hint_y=.1, spacing=5)
        self.topbuttonsgrid.add_widget(self.backbutton)
        self.topbuttonsgrid.add_widget(self.updatebutton)
        self.deleteallbutton = Button(text=Settings().text('Apagar todos os eventos'), size_hint_y=.1, on_release=self.deleteallevents, markup=True, background_color=Settings().secundaria(), background_normal='')
        
        # Lado esquerdo
        self.scrollgrid = GridLayout(cols=1, spacing=10)
        self.scrollgrid.add_widget(self.topbuttonsgrid)
        self.scrollgrid.add_widget(self.scroll)
        self.scrollgrid.add_widget(self.deleteallbutton)

        # Juntando os dois lados
        self.grid = GridLayout(cols=2, spacing=100, pos_hint={'x': .05, 'y': .05}, size_hint=(.90, .90))
        self.grid.add_widget(self.scrollgrid) 
        self.detailsgrid = DetailsGrid(self)
        self.grid.add_widget(self.detailsgrid)
        self.add_widget(self.grid)

    def update(self, button=Button()):
        ''' Atualiza as informações da tela '''
        self.clear_widgets()
        self.draw()

    def deleteallevents(self, button):
        ''' Deleta todos os eventos do arquivo '''
        deleteall()
        Lista_Eventos.parent.update()

    def backtohome(self, button):
        ''' Volta para a tela inicial '''
        Lista_Eventos.parent.current='ClimaEventos'

Lista_Eventos = ListaEventos()
