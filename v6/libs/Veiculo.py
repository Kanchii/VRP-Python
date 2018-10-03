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

        if(self.tempo_Total + tempo_Viagem < cliente.comeca):
            self.tempo_Total = cliente.comeca + cliente.tempo_Servico
        else:
            self.tempo_Total += tempo_Viagem + cliente.tempo_Servico
        
        self.clientes.append(cliente)
    
    def simula(self):
        import Global

        fitness = 0
        carregando = 0
        tempo_Total = 0
        for i in range(1, len(self.clientes)):

            # Verificando regra de capacidade
            if(carregando + self.clientes[i].demanda > Global.capacidade_Veiculo):
                return -1

            tempo_Viagem =  Global.matriz_Distancia[self.clientes[i - 1].id][self.clientes[i].id]
            tempo_Viagem_Deposito = Global.matriz_Distancia[self.clientes[i].id][Global.deposito.id]

            # Verificando se nao chega depois do limite do cliente
            if(tempo_Total + tempo_Viagem > self.clientes[i].termina):
                return -1
            
            # Verificando se consegue ainda chegar no deposito
            if(tempo_Total + tempo_Viagem < self.clientes[i].comeca):
                if(self.clientes[i].comeca + self.clientes[i].tempo_Servico + tempo_Viagem_Deposito > Global.deposito.termina):
                    return -1
            else:
                if(tempo_Total + tempo_Viagem + self.clientes[i].tempo_Servico + tempo_Viagem_Deposito > Global.deposito.termina):
                    return -1
            
            carregando += self.clientes[i].demanda
            fitness += tempo_Viagem
            if(tempo_Total + tempo_Viagem < self.clientes[i].comeca):
                tempo_Total = self.clientes[i].comeca + self.clientes[i].tempo_Servico
            else:
                tempo_Total += tempo_Viagem + self.clientes[i].tempo_Servico

        return fitness

    def OPT_2(self):
        flag = True
        while(flag):
            flag = False
            for i in range(1, len(self.clientes) - 2):
                for j in range(1, len(self.clientes) - 2):
                    if(abs(i - j) < 2): continue
                    self.clientes[i + 1], self.clientes[j] = self.clientes[j], self.clientes[i + 1]
                    tmp = self.simula()
                    if(tmp >= 0 and tmp < self.fitness):
                        self.fitness = tmp
                        flag = True
                    else:
                        self.clientes[i + 1], self.clientes[j] = self.clientes[j], self.clientes[i + 1]
