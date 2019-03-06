class Veiculo:
    def __init__(self, id):
        import Global

        self.clientes = [Global.deposito]
        self.fitness = 0
        self.id = id
        self.tempo_Total = 0
        self.carregando = 0
        self.custo = 0
        # self.carregamentoMorto = 0
    
    # Verifica em qual posicao eh melhor alocar um cliente dentro da rota 
    def quebra_Regra_Artigo(self, cliente):
        import copy

        fitness = 1e9
        pos = -1
        self.carregando += cliente.demanda

        for i in range(1, len(self.clientes) + 1):
            self.clientes = self.clientes[:i] + [cliente] + self.clientes[i:]
            tmp = self.simula()
            # print(tmp)
            if(tmp > -1):
                if(tmp < fitness):
                    fitness = tmp
                    pos = i
            self.clientes = self.clientes[:i] + self.clientes[i + 1:]
        # print(pos)
        self.carregando -= cliente.demanda
        return pos            
    
    # Verifica se pegando um cliente e adicionando ele ao final da rota nao ha quebra de restricao
    def quebra_Regra(self, cliente):
        import Global

        # Verificando regra de capacidade
        if(self.carregando + cliente.demanda > Global.veiculos_Capacidades[self.id][0]):
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
    
    # Adiciona um cliente em uma posicao especifica
    def add_Artigo(self, cliente, pos):
        import Global

        self.clientes = self.clientes[:pos] + [cliente] + self.clientes[pos:]
        self.carregando += cliente.demanda
        self.fitness = self.simula()

        tempo = 0
        for i in range(1, len(self.clientes)):
            tempo_Viagem = Global.matriz_Distancia[self.clientes[i - 1].id][self.clientes[i].id]
            if(tempo + tempo_Viagem < self.clientes[i].comeca):
                tempo = self.clientes[i].comeca + self.clientes[i].tempo_Servico
            else:
                tempo += tempo_Viagem + self.clientes[i].tempo_Servico
        self.tempo_Total = tempo            

    # Adiciona um cliente no final da rota
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

    # Simula para a configuracao atual se a rota eh viavel
    def simula(self):
            import Global

            fitness = 0
            carregando = self.carregando
            if(carregando > Global.veiculos_Capacidades[self.id][0]):
                return -1
            pesoMorto = 0
            tempo_Total = 0
            for i in range(1, len(self.clientes)):

                # Verificando regra de capacidade + P&D
                if(carregando - self.clientes[i].demanda + self.clientes[i].coleta + pesoMorto > Global.veiculos_Capacidades[self.id][0]):
                    # print("Estourou a capacidade")
                    return -1

                tempo_Viagem = Global.matriz_Distancia[self.clientes[i - 1].id][self.clientes[i].id]
                tempo_Viagem_Deposito = Global.matriz_Distancia[self.clientes[i].id][Global.deposito.id]

                # Verificando se nao chega depois do limite do cliente
                if(tempo_Total + tempo_Viagem > self.clientes[i].termina):
                    # print("Estourou a janela de tempo")
                    return -1

                # Verificando se consegue ainda chegar no deposito
                if(tempo_Total + tempo_Viagem < self.clientes[i].comeca):
                    if(self.clientes[i].comeca + self.clientes[i].tempo_Servico + tempo_Viagem_Deposito > Global.deposito.termina):
                        # print("Nao consigo voltar para o depot")
                        return -1
                else:
                    if(tempo_Total + tempo_Viagem + self.clientes[i].tempo_Servico + tempo_Viagem_Deposito > Global.deposito.termina):
                        # print("Tmb nao consigo voltar para o depot")
                        return -1

                carregando -= self.clientes[i].demanda
                pesoMorto += self.clientes[i].coleta
                fitness += tempo_Viagem
                if(tempo_Total + tempo_Viagem < self.clientes[i].comeca):
                    tempo_Total = self.clientes[i].comeca + \
                        self.clientes[i].tempo_Servico
                else:
                    tempo_Total += tempo_Viagem + self.clientes[i].tempo_Servico

            return fitness

    # Heuristica de otimizacao local para refinamento da resposta
    def OPT_2(self, perc):
        import random
        flag = True
        for k in range(flag):
            flag = False
            for i in range(1, len(self.clientes) - 2):
                for j in range(1, len(self.clientes) - 2):
                    if(abs(i - j) < 2): continue
                    self.clientes[i + 1], self.clientes[j] = self.clientes[j], self.clientes[i + 1]
                    tmp = self.simula()
                    aux = random.uniform(0, 1)
                    # if(tmp >= 0):
                    #     print("Carai")
                    if((tmp >= 0 and aux < perc) or (tmp >= 0 and tmp < self.fitness)):
                        # if(tmp >= 0 and aux < perc):
                        #     print("Aceitou solucao pior")
                        print("oi")
                        self.fitness = tmp
                        flag = True
                    else:
                        self.clientes[i + 1], self.clientes[j] = self.clientes[j], self.clientes[i + 1]
