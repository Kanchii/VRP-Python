class Veiculo:
    def __init__(self, id):
        import Global

        self.clientes = [Global.deposito]
        self.fitness = 0
        self.id = id
        self.tempo_Total = 0
        self.carregando = 0
    
    def quebra_Regra(self, cliente):
        import Global

        # Verificando regra de capacidade
        if(self.carregando + cliente.demanda > Global.capacidade_Veiculo):
            return True
        
        tempo_Viagem =  Global.matriz_Distancia[self.clientes[-1].id][cliente.id]
        tempo_Viagem_Deposito = Global.matriz_Distancia[cliente.id][Global.deposito.id]

        # Verificando se nao chega depois do limite do cliente
        if(self.tempo_Total + tempo_Viagem > cliente.termina):
            return True
        
        # Verificando se consegue ainda chegar no deposito
        if(self.tempo_Total + tempo_Viagem < cliente.comeca):
            if(cliente.comeca + cliente.tempo_Servico + tempo_Viagem_Deposito > Global.deposito.termina):
                return True
        else:
            if(self.tempo_Total + tempo_Viagem + cliente.tempo_Servico + tempo_Viagem_Deposito > Global.deposito.termina):
                return True
        
        return False
    
    def add(self, cliente):
        import Global

        self.carregando += cliente.demanda

        tempo_Viagem = Global.matriz_Distancia[self.clientes[-1].id][cliente.id]

        self.fitness += tempo_Viagem

        if(self.tempo_Total + tempo_Viagem <= cliente.comeca):
            self.tempo_Total = cliente.comeca + cliente.tempo_Servico
        else:
            self.tempo_Total += tempo_Viagem + cliente.tempo_Servico
        
        self.clientes.append(cliente)