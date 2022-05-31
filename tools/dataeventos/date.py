from datetime import date

class Date:
    ''' Classe que guarda uma data '''

    def __init__(self, day = 1, month = 1, year = 1980, date = None):
        if date != None:
            self.__day = date.getDay()
            self.__month = date.getMonth()
            self.__year = date.getYear()

        elif self.verifyDate(day, month, year):
            self.__day = day
            self.__month = month
            self.__year = year
            

    def verifyDate(self, day, month, year):
        ''' Função que verifica se é uma data válida '''
        if (day < 1 or day > 31) or (month <1 or month > 12) or (year < 1):
            return False
        elif (month == 4 or month == 6 or month == 9 or month == 11) and (day > 30):
            return False
        elif (month == 2) and (day > 29):
            return False
        elif ((year % 4 != 0) or ((year % 100 == 0) and (year % 400 != 0))) and (day > 28 and month == 2):
            return False
        else:
            return True

    #Funções que retornam a data
    def getDate(self):
        ''' Função que retorna uma cópia da variável no tipo Date() '''

        return Date(self.getDay(), self.getMonth(), self.getYear())
    
    def getDay(self):
        ''' Função que retorna o dia '''

        return self.__day

    def getMonth(self):
        ''' Função que retorna o mês '''

        return self.__month

    def getYear(self):
        ''' Função que retorna o ano '''

        return self.__year
    
    def getDateNow(self):
        ''' Função que retorna uma variável do tipo Date com a data do dia atual '''

        today = date.today()
        day = today.day
        month = today.month
        year = today.year

        return Date(day, month, year)

    def setDate(self, day, month, year):
        ''' Função utilizada para definir a data '''

        if self.verifyDate(day, month, year):
            self.__day = day
            self.__month = month
            self.__year = year
    
    def setday(self, day):
        ''' Função utilizada para definir o dia '''

        if self.verifyDate(day, self.__month, self.__year):
            self.__day = day

    def setmonth(self, month):
        ''' Função utilizada para definir o mês '''

        if self.verifyDate(self.__day, month, self.__year):
            self.__month = month

    def setyear(self, year):
        ''' Função utilizada para definir o ano '''

        if self.verifyDate(self.__day, self.__month, year):
            self.__year = year

    def addDays(self, ndays):
        ''' Função que adiciona um número de dias à data '''
        
        modif = 1
        self.__day += ndays
        if ndays > 0:
            while modif > 0:
                if ((self.__month == 4) or (self.__month == 6) or (self.__month == 9) or (self.__month == 11)) and (self.__day > 30):
                    self.__month += 1
                    self.__day -= 30
                    modif += 1
                elif ((self.__month == 1) or (self.__month == 3) or (self.__month == 5) or (self.__month == 7) or (self.__month == 8) or (self.__month == 10) or (self.__month == 12)) and (self.__day > 31):
                    self.__month += 1
                    self.__day -= 31
                    modif += 1
                elif ((self.__month == 2) and not((self.__year % 4 != 0)) or ((self.__year % 100 == 0) and (self.__year % 400 != 0))) and (self.__day > 29):
                    self.__month += 1
                    self.__day -= 29
                    modif += 1
                elif (self.__month == 2) and (self.__day > 28) and ((self.__year % 4 != 0)) or ((self.__year % 100 == 0) and (self.__year % 400 != 0)):
                    self.__month += 1
                    self.__day -= 28   
                    modif += 1
                if(self.__month > 12):
                    self.__month = 1
                    self.__year += 1
                modif -= 1

        if ndays < 0:
            modif = 1
            while modif > 0:
                if ((self.__month == 1) or (self.__month == 2) or (self.__month == 4) or (self.__month == 6) or (self.__month == 8) or (self.__month == 9) or (self.__month == 11)) and (self.__day < 1):
                    self.__month -=1 
                    self.__day += 31
                    modif += 1
                elif ((self.__month == 5) or (self.__month == 7) or (self.__month == 10) or (self.__month == 12)) and (self.__day < 1):
                    self.__month -= 1
                    self.__day += 30
                    modif += 1
                elif ((self.__month == 3) and not((self.__year % 4 != 0)) or ((self.__year % 100 == 0) and (self.__year % 400 != 0))) and (self.__day < 1):
                    self.__month -= 1
                    self.__day += 29
                    modif += 1
                elif (self.__month == 3) and (self.__day < 1) and ((self.__year % 4 != 0)) or ((self.__year % 100 == 0) and (self.__year % 400 != 0)):
                    self.__month -= 1
                    self.__day += 28   
                    modif += 1
                if(self.__month < 1):
                    self.__month = 12
                    self.__year -= 1
                modif -= 1

    def compareDate(self, day, month, year, date = None):
        ''' Função que compara duas datas '''
    
        if date != None:
            day = date.getDay()
            month = date.getMonth()
            year = date.getYear()

        if day == self.__day and month == self.__month and year == self.__year:
            return True
        else:
            return False

    def isBefore(self, otherDate):
        ''' Função que verifica se a data enviada como parâmetro é anterior a data '''

        if otherDate.getYear() > self.__year:
            return True
        elif otherDate.getYear() == self.__year and otherDate.getMonth() > self.__month:
            return True 
        elif otherDate.getYear() == self.__year and otherDate.getMonth() == self.__month and otherDate.getDay() > self.__day:
            return True
        else:
            return False

    def daysTo(self, otherDate):
        ''' Retorna o número de dias entre uma data e outra '''
    
        contDays = 0

        pre = Date(date=self.getDate())
        post = Date(date=otherDate.getDate())   
        if pre.isBefore(post):
            pre = Date(date=otherDate.getDate())
            post = Date(date=self.getDate())


        contDays = (post.getYear()-pre.getYear()-1)*365
        pre.addDays(contDays)

        while post.getDay() != pre.getDay() or post.getMonth() != pre.getMonth() or post.getYear() != pre.getYear():
            pre.addDays(1)
            contDays += 1

        return contDays
        
    def weekDayStr(self):
        ''' Retorna o dia da semana da data em forma de string '''

        key = self.weekDayInt
        
        weekDic = {0: 'Domingo', 1: 'Segunda-feira', 2: 'Terça-feira', 3: 'Quarta-feira', 4: 'Quinta-feira', 5: 'Sexta-feira', 6: 'Sábado'}
        
        return weekDic[key]

    def weekDayInt(self):
        ''' Retorna o dia da dsemana da data em forma de int '''

        ref = Date(1, 12, 2019)
        key = ref.daysTo(self) % 7

        if ref.isBefore(self):
            key = (key-7)*-1


        return key
        
    def __str__(self):
        return str(self.__day) + "/" + str(self.__month) + "/" + str(self.__year)    



if __name__ == "__main__":
    def main():
        date = Date(30, 11, 2019)

        print(date.weekDayInt())

    main()