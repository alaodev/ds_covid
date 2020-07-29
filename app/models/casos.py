class Casos():
    def __init__(self, id, data, uf, conf, mortes):
        self.id = id
        self.data = data
        self.uf = uf
        self.confirmados = conf
        self.mortes = mortes

class Frequencias():
    def __init__(self, data, frequencia):
        self.data = data
        self.frequencia = frequencia