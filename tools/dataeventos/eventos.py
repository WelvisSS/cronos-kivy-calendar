from tools.dataeventos.date import Date
import os

def createevent(date, event='Evento', description='Descrição do evento'):
    ''' Recebe como parametro uma data, um evento e a descrição desse evento e escreve os dados em um arquivo, sobrescrevendo um evento anteriormente atribuido à mesma data '''

    if not(os.path.isfile("assets/source/arquivo_com_eventos.txt")):
        deleteall()

    deleteevent(date)

    with open("assets/source/arquivo_com_eventos.txt", "a") as file:
        file.write(event.strip() + "-" + str(date.getDay()) + "/" + str(date.getMonth()) + "/" + str(date.getYear()) + "-" + description.strip() + "\n")


def deleteevent(date):
    ''' Recebe como parametro uma data, um evento e a descrição desse evento e apaga do arquivo com os dados de evento '''
    
    with open("assets/source/arquivo_com_eventos.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)

        for line in lines:
            linesplit = line.split('-')
            datesplit = linesplit[1].split('/')

            if date.getDay() != int(datesplit[0]) or date.getMonth() != int(datesplit[1]) or date.getYear() != int(datesplit[2]):
                file.write(line)
        
        file.truncate()

def deleteall():
    ''' Exclui todos os eventos do arquivo '''

    open("assets/source/arquivo_com_eventos.txt", "w")   


def listevents():
    ''' Retorna uma lista com os dados de todas as datas do arquivo de dados de evento '''

    if not(os.path.isfile("assets/source/arquivo_com_eventos.txt")):
        deleteall()

    with open("assets/source/arquivo_com_eventos.txt", "r") as file:
        lines = file.readlines()
        return lines


def getdateevent(date):
    ''' Retorna os eventos de uma data específica '''
    
    if not(os.path.isfile("assets/source/arquivo_com_eventos.txt")):
        deleteall()

    lista = listevents()

    for event in lista:
        eventsplit = event.split('-')
        datesplit = eventsplit[1].split('/')

        if date.getDay() == int(datesplit[0]) and date.getMonth() == int(datesplit[1]) and date.getYear() == int(datesplit[2]):
            return event.strip()

def eventsperiod(start, end):
    ''' Retorna uma lista com todas as datas que estão entre as datas definidas '''
    
    events = []

    lines = listevents()
    for line in lines:
        splitline = line.split('-')
        date = splitline[1].split('/')
        date = Date(int(date[0]), int(date[1]), int(date[2]))

        if not(date.isBefore(start)) and date.isBefore(end):
            events.append(line)

    return events
    
def hasevent(date):
    ''' Recebe um dia, mês e ano e retorna verdadeiro caso exista um evento '''
    events = listevents()

    for event in events:
        eventsplit = event.split('-')
        datesplit = eventsplit[1].split('/')
        if int(datesplit[0]) == date.getDay() and int(datesplit[1]) == date.getMonth() and int(datesplit[2]) == date.getYear():
            return True

    return False


if __name__ == "__main__":
    createevent(Date(1, 1, 2000), "evento", "evento")
    createevent(Date(1, 1, 2001), "evento", "evento")
    createevent(Date(1, 1, 2002), "evento", "evento")