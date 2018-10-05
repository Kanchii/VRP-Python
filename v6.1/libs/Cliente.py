class Cliente:
    def __init__(self, pos, id, demanda, time_Window):
        self.pos = pos
        self.id = id
        self.demanda = demanda
        self.comeca = time_Window[0]
        self.termina = time_Window[1]
        self.tempo_Servico = time_Window[2]
