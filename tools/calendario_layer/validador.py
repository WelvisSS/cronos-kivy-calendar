def valida_mes(mes):
    if 0 < int(mes) and int(mes) <= 12:
        return True
    else:
        return False

def valida_ano(ano):
    if int(ano)<1901:
        return False
    else:
        return True