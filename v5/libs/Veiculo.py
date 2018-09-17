class Veiculo:
    def __init__(self, id, capacidade):
        self.id = id
        self.capacidade = capacidade
        self.rota = []
        self.carregando = 0
        self.tempo = 0
