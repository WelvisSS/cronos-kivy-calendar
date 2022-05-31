from kivy.app import App
from  kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout 
from datetime import datetime
from tools.config import Settings 
import requests as rq #Referente aos dados climáticos
import socket

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
confiaveis = ['www.google.com', 'www.yahoo.com', 'www.bb.com.br']

def check_host():
    global confiaveis
    for host in confiaveis:
        a=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a.settimeout(.5)
        try:
            b=a.connect_ex((host, 80))
            if b==0: #ok, conectado
                return True
        except:
            pass
        a.close()
    return False

#Se check_host for True entra no if senão coloca ??? nas entradas        
if(check_host()):
    class ClimaTempo():
        def __init__(self, cidade='Ilhéus'):
            self.__cidade = cidade

        def clima(self):	
            endereco_api = "http://api.openweathermap.org/data/2.5/weather?appid=9e1280f88eef9db700e867bb898fd3ec&q=" #Link que permite buscar informações climáticas 
            url = endereco_api + self.__cidade #Basta adicionar o nome da cidade desejada em ferente ao link para obter suas informações climáticas

            infos = rq.get(url).json() #Utilização do modelo Json para extrair as informações da url que é adicionada
            
            if str(infos) != str({'cod': '404', 'message': 'city not found'}) :
                #Coordendas
                #Extração dos dados baseados nas strings que são passadas
                longitude    = infos['coord']['lon']
                latitude     = infos['coord']['lat']
                temp         = infos['main']['temp'] - 273.15 #Como a temperatura climática vem em Kelvin basta subtrair 273.15 para converter para Celsius
                pressao_atm  = infos['main']['pressure'] / 1013.25 #Conversão Libras para ATM
                humidade     = infos['main']['humidity'] # Recebe em porcentagem
                temp_max     = infos['main']['temp_max'] - 273.15 #Conversão Kelvin para Celsius
                temp_min     = infos['main']['temp_min'] - 273.15 #Conversão Kelvin para Celsius
                #vento
                v_speed      = infos['wind']['speed'] # km/h
                v_direc      = infos['wind']['deg'] #Recebe em graus
                #nuvens
                nebulosidade = infos['clouds']['all']
                #id
                id_da_cidade = infos['id']#ID referente a cidade pela qual são capturadas as informações climáticas

                return [longitude, latitude, temp, pressao_atm, humidade, temp_max, temp_min, v_speed, v_direc, nebulosidade, id_da_cidade, self.__cidade]
            else:
                self.__cidade = 'Ilhéus'
                endereco_api = "http://api.openweathermap.org/data/2.5/weather?appid=9e1280f88eef9db700e867bb898fd3ec&q=" #Link que permite buscar informações climáticas 
                url = endereco_api + self.__cidade #Basta adicionar o nome da cidade desejada em ferente ao link para obter suas informações climáticas

                infos = rq.get(url).json() #Utilização do modelo Json para extrair as informações da url que é adicionada
                #Coordendas
                #Extração dos dados baseados nas strings que são passadas
                longitude    = infos['coord']['lon']
                latitude     = infos['coord']['lat']
                temp         = infos['main']['temp'] - 273.15 #Como a temperatura climática vem em Kelvin basta subtrair 273.15 para converter para Celsius
                pressao_atm  = infos['main']['pressure'] / 1013.25 #Conversão Libras para ATM
                humidade     = infos['main']['humidity'] # Recebe em porcentagem
                temp_max     = infos['main']['temp_max'] - 273.15 #Conversão Kelvin para Celsius
                temp_min     = infos['main']['temp_min'] - 273.15 #Conversão Kelvin para Celsius
                #vento
                v_speed      = infos['wind']['speed'] # km/h
                v_direc      = infos['wind']['deg'] #Recebe em graus
                #nuvens
                nebulosidade = infos['clouds']['all']
                #id
                id_da_cidade = infos['id']#ID referente a cidade pela qual são capturadas as informações climáticas

                return [longitude, latitude, temp, pressao_atm, humidade, temp_max, temp_min, v_speed, v_direc, nebulosidade, id_da_cidade, self.__cidade]
    
        def temperatura(self):
            temp_atual = self.clima()[2]
            temp_max   = self.clima()[5]
            temp_min   = self.clima()[6]
            
            return [temp_atual, temp_max, temp_min]

    Configuracoes = Settings()
    City = str(Configuracoes.localizacao())
    City = City.strip('\n')

    if City == '':
        Clima         = ClimaTempo()
    else:
        Clima         = ClimaTempo(City)
    
    lista         = Clima.clima()
    lista        += Clima.temperatura()
    temp          = lista[2]
    pressao_atm   = lista[3]
    humidade      = lista[4]
    v_speed       = lista[7]
    nebulosidade  = lista[9]
    cidade        = lista[11]

    Temperatura   = ('{:.0f}º'.format(temp))
    Humid         = ("{}%".format(humidade))
    Neb           = ("{:.0f}%".format(nebulosidade))
    Vel_ven       = ("{} m/s".format(v_speed))
    Pres_At       = ("{:.1f} atm".format(pressao_atm))
    
else:
    #Caso não seja estabelecida a conexão com a rede
    cidade        = 'Sem Conexão!'
    Temperatura   = ('?')
    Humid         = ('?')
    Neb           = ('?')
    Vel_ven       = ('?')
    Pres_At       = ('?')
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

class LayoutClima(FloatLayout, App):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        now = datetime.now()

        if (((now.hour > 18 or now.hour == 18) and (now.hour < 23 or now.hour == 23)) or ((now.hour > 00 or now.hour == 00) and (now.hour < 6 or now.hour == 6))):
            if(((now.hour > 4 or now.hour == 4) and (now.hour < 5 or now.hour == 5))):
                fundo = 3
            else:
                fundo = 2
        else:
            if(((now.hour > 16 or now.hour == 16) and (now.hour < 17 or now.hour == 17))):
                fundo = 4
            else:
                fundo = 1
        #DIA
        if fundo == 1:
            self.add_widget(Image(source='assets/dia.png'))
            self.add_widget(Label(text=str(cidade), color= [0,0,0,3.0], font_size=35, pos_hint={'x':-0.16, 'y':0.43}))
            self.add_widget(Label(text=Temperatura, color= [0,0,0,3.0], font_size=60, pos_hint={'x':-0.15, 'y':0.3}))
            self.add_widget(Label(text=Humid, color= [0,0,0,3.0], font_size=30, pos_hint={'x':-0.10, 'y':0.11}))
            self.add_widget(Label(text=Neb, font_size=30, pos_hint={'x':-0.41, 'y':-0.42}))
            self.add_widget(Label(text=Vel_ven, font_size=30, pos_hint={'x':-0.25, 'y':-0.42}))
            self.add_widget(Label(text=Pres_At, font_size=30, pos_hint={'x':-0.09, 'y':-0.42}))
        #NOITE
        if fundo == 2:
            self.add_widget(Image(source='assets/noite.png'))
            self.add_widget(Label(text=str(cidade), font_size=35, pos_hint={'x':-0.16, 'y':0.43}))
            self.add_widget(Label(text=Temperatura, font_size=60, pos_hint={'x':-0.15, 'y':0.3}))
            self.add_widget(Label(text=Humid, font_size=30, pos_hint={'x':-0.10, 'y':0.11}))
            self.add_widget(Label(text=Neb, font_size=30, pos_hint={'x':-0.41, 'y':-0.42}))
            self.add_widget(Label(text=Vel_ven, font_size=30, pos_hint={'x':-0.25, 'y':-0.42}))
            self.add_widget(Label(text=Pres_At, font_size=30, pos_hint={'x':-0.09, 'y':-0.42}))
        #MANHÃ
        if fundo == 3:
            self.add_widget(Image(source='assets/matina.png'))
            self.add_widget(Label(text=str(cidade), color= [0,0,0,3.0], font_size=35, pos_hint={'x':-0.2, 'y':0.43}))
            self.add_widget(Label(text=Temperatura, color= [0,0,0,3.0], font_size=60, pos_hint={'x':-0.2, 'y':0.3}))
            self.add_widget(Label(text=Humid, color= [0,0,0,3.0], font_size=30, pos_hint={'x':-0.10, 'y':0.11}))
            self.add_widget(Label(text=Neb, font_size=30, pos_hint={'x':-0.41, 'y':-0.42}))
            self.add_widget(Label(text=Vel_ven, font_size=30, pos_hint={'x':-0.25, 'y':-0.42}))
            self.add_widget(Label(text=Pres_At, font_size=30, pos_hint={'x':-0.09, 'y':-0.42}))
        #TARDE
        if fundo == 4:
            self.add_widget(Image(source='assets/tarde.png'))
            self.add_widget(Label(text=str(cidade), color= [0,0,0,3.0], font_size=35, pos_hint={'x':-0.16, 'y':0.43}))
            self.add_widget(Label(text=Temperatura, color= [0,0,0,3.0], font_size=60, pos_hint={'x':-0.15, 'y':0.3}))
            self.add_widget(Label(text=Humid, color= [0,0,0,3.0], font_size=30, pos_hint={'x':-0.10, 'y':0.11}))
            self.add_widget(Label(text=Neb, font_size=30, pos_hint={'x':-0.41, 'y':-0.42}))
            self.add_widget(Label(text=Vel_ven, font_size=30, pos_hint={'x':-0.25, 'y':-0.42}))
            self.add_widget(Label(text=Pres_At, font_size=30, pos_hint={'x':-0.09, 'y':-0.42}))


ObjLayoutClima = LayoutClima()