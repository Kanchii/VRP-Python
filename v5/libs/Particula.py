class Particula:
    def __init__(self, numClientes, capacidade, coords, demandas, timeWindow, matrizDistancia):
        import random, copy, numpy as np
        from libs.Cliente import Cliente

        self.numClientes = numClientes
        self.numVeiculos = self.numClientes
        self.capacidade = capacidade
        # self.coords = coords
        # self.demandas = demandas
        # self.timeWindow = timeWindow
        self.clientes = []
        for i in range(0, self.numClientes + 1):
            self.clientes.append(Cliente(i, demandas[i], timeWindow[i][0], timeWindow[i][1],
                                         timeWindow[i][2], coords[i]))
            # print(self.clientes[i].id, self.clientes[i].demanda, self.clientes[i].inicioJanela, self.clientes[i].terminoJanela, self.clientes[i].tempoServico, self.clientes[i].coord)
        self.deposito = Cliente(0, demandas[0], timeWindow[0][0], timeWindow[0][1],
                                timeWindow[0][2], coords[0])
        self.matrizDistancia = matrizDistancia

        self.alpha = 2 # Fator Cognitivo
        self.beta = 2 # Fator Social
        self.inercia = 0.9 # Fator de inercia
        self.inerciaInicial = self.inercia
        self.inerciaFinal = 0.1

        self.maxClienteVel = 100000
        self.minClienteVel = -100000
        self.maxClientePos = 100000
        self.minClientePos = -100000
        self. maxVeiculoX, self.minVeiculoX = -1e9, 1e9
        self.maxVeiculoY, self.minVeiculoY = -1e9, 1e9
        for cliente in [self.deposito] + self.clientes:
            self.maxVeiculoX = max(self.maxVeiculoX, cliente.coord[0])
            self.minVeiculoX = min(self.minVeiculoX, cliente.coord[0])
            self.maxVeiculoY = max(self.maxVeiculoY, cliente.coord[1])
            self.minVeiculoY = min(self.minVeiculoY, cliente.coord[1])

        self.posicao = np.array([random.uniform(-100000, 100000) for _ in range(self.numClientes)])
        for _ in range(self.numVeiculos):
            self.posicao = np.append(self.posicao, random.uniform(self.minVeiculoX, self.maxVeiculoX))
            self.posicao = np.append(self.posicao, random.uniform(self.minVeiculoY, self.maxVeiculoY))
        self.velocidade = np.array([0 for _ in range(self.numClientes + 2 * self.numVeiculos)])
        self.pbest = copy.deepcopy(self.posicao)
        self.fitness = self.calculaFitness()
        self.gbest = None

    def aplicaAjuste(self):
        for i in range(self.numClientes):
            self.velocidade[i] = max(self.minClienteVel, min(self.velocidade[i], self.maxClienteVel))
            self.posicao[i] = max(self.minClientePos, min(self.posicao[i], self.maxClientePos))

        for i in range(self.numClientes, self.numClientes + 2 * self.numVeiculos, 2):
            if(self.velocidade[i] < -self.maxVeiculoX):
                self.velocidade[i] = -self.maxVeiculoX
            elif(self.velocidade[i] > self.maxVeiculoX):
                self.velocidade[i] = self.maxVeiculoX
            # self.velocidade[i] = max(-self.maxVeiculoX, min(self.velocidade[i], self.maxVeiculoX))
            # self.velocidade[i + 1] = max(-self.maxVeiculoY, min(self.velocidade[i + 1], self.maxVeiculoY))
            self.posicao[i] = max(self.minVeiculoX, min(self.posicao[i], self.maxVeiculoX))
            self.posicao[i + 1] = max(self.minVeiculoY, min(self.posicao[i + 1], self.maxVeiculoY))

    def atualizaVelocidade(self, iteracaoAtual, iteracaoMaxima):
        import random

        r1, r2 = random.uniform(0, 1), random.uniform(0, 1)
        self.velocidade = self.inercia * self.velocidade + \
                          self.alpha * r1 * (self.pbest - self.posicao) + \
                          self.beta * r2 * (self.gbest - self.posicao)

        # print(self.inercia * self.velocidade)
        # print(self.alpha * r1 * (self.pbest - self.posicao))
        # print(self.beta * r2 * (self.gbest - self.posicao))

        self.inercia = self.inerciaFinal + (iteracaoMaxima - iteracaoAtual) * (self.inerciaInicial - self.inerciaFinal) / float(iteracaoMaxima)
        # print(self.inercia)
        # print("Antes: ", self.velocidade)
        self.aplicaAjuste()
        # print("Depois: ", self.velocidade)

    def atualizaPosicao(self):
        import copy

        self.posicao += self.velocidade

        # print(self.posicao[self.numClientes:])
        # print("\n\n")

        self.aplicaAjuste()

    def violaRegra(self, veiculo, cliente):
        ''' Verificando se a capacidade do veiculo nao sera excedida '''
        if(veiculo.carregando + cliente.demanda > veiculo.capacidade):
            # print("Quebrou a capacidade")
            return True

        dist = self.matrizDistancia[veiculo.rota[-1]][cliente.id] #Ultimo lugar ate o cliente
        distAteDeposito = self.matrizDistancia[cliente.id][self.deposito.id]
        ''' Verificando se respeita a janela de tempo '''

        #Verificando se nao vai chegar depois do tempo maximo
        if(veiculo.tempo + dist > cliente.terminoJanela):
            # print("Quebrou o tempo maximo")
            return True

        # Verificando se consegue ir ate o cliente e depois voltar para o deposito
        if(veiculo.tempo + dist < cliente.inicioJanela):
            if(cliente.inicioJanela + cliente.tempoServico + distAteDeposito > self.deposito.terminoJanela):
                # print("Quebrou o tempo maximo do deposito")
                return True
        else:
            if(veiculo.tempo + dist + cliente.tempoServico + distAteDeposito > self.deposito.terminoJanela):
                # print("Quebrou o tempo maximo do deposito")
                return True
        return False

    def geraRota(self, vetorPosicao = None):
        from libs.Veiculo import Veiculo

        if(vetorPosicao is None):
            vetorPrioridadeClientes = self.geraVetorPrioridadeClientes()
            matrizPrioridadeVeiculos = self.geraMatrizPrioridadeVeiculos()
        else:
            vetorPrioridadeClientes = self.geraVetorPrioridadeClientes(vetorPosicao)
            matrizPrioridadeVeiculos = self.geraMatrizPrioridadeVeiculos(vetorPosicao)

        veiculos = [Veiculo(i, self.capacidade) for i in range(self.numVeiculos + 1)]
        for i in range(self.numVeiculos + 1):
            veiculos[i].rota.append(self.deposito.id)
        for indiceCliente in vetorPrioridadeClientes:
            cliente = self.clientes[indiceCliente[0]]
            for indiceVeiculo in matrizPrioridadeVeiculos[cliente.id]:
                veiculo = veiculos[indiceVeiculo[1]]
                if(not self.violaRegra(veiculo, cliente)):
                    dist = self.matrizDistancia[veiculo.rota[-1]][cliente.id]
                    if(veiculo.tempo + dist < cliente.inicioJanela):
                        veiculos[veiculo.id].tempo = cliente.inicioJanela + cliente.tempoServico
                    else:
                        veiculos[veiculo.id].tempo = veiculos[veiculo.id].tempo + (dist + cliente.tempoServico)
                    veiculos[veiculo.id].rota.append(cliente.id)
                    veiculos[veiculo.id].carregando += cliente.demanda
                    break
        for i in range(self.numVeiculos + 1):
            veiculos[i].rota.append(self.deposito.id)

        return veiculos

    def calculaFitness(self):
        veiculos = self.geraRota()
        fitness = 0
        for veiculo in veiculos:
            if(len(veiculo.rota) > 2):
                for i in range(1, len(veiculo.rota)):
                    indiceAnt = veiculo.rota[i - 1]
                    indiceAtual = veiculo.rota[i]
                    dist = self.matrizDistancia[indiceAnt][indiceAtual]
                    fitness += dist
        return fitness

    def geraVetorPrioridadeClientes(self, vetorPosicao = None):
        if(vetorPosicao is None):
            clientes = [(indice + 1, prioridade) for (indice, prioridade) in enumerate(self.posicao[:self.numClientes])]
        else:
            clientes = [(indice + 1, prioridade) for (indice, prioridade) in enumerate(vetorPosicao[:self.numClientes])]
        clientes = sorted(clientes, key = lambda u : u[1])
        # print(clientes)
        return clientes

    def geraMatrizPrioridadeVeiculos(self, vetorPosicao = None):
        matrizClientes = [[] for i in range(self.numClientes + 1)]

        def euclidianDistance(a, b):
            from math import sqrt
            return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        for i in range(self.numClientes, self.numClientes + 2 * self.numVeiculos, 2):
            if(vetorPosicao is None):
                veiculoCoord = (self.posicao[i], self.posicao[i + 1])
            else:
                veiculoCoord = (vetorPosicao[i], vetorPosicao[i + 1])
            for cliente in self.clientes:
                dist = euclidianDistance(veiculoCoord, cliente.coord)
                matrizClientes[cliente.id].append((dist, (i - self.numClientes) // 2))
        for i in range(self.numClientes + 1):
            matrizClientes[i] = sorted(matrizClientes[i], key = lambda u : u[0])
        # print(matrizClientes[0])
        return matrizClientes

    def calculaFitnessRotaOnly(self, rota):
        fit = 0
        for i in range(1, len(rota)):
            fit += self.matrizDistancia[rota[i - 1]][rota[i]]
        return fit

    def violaRegraOnly(self, rota):
        from libs.Veiculo import Veiculo

        veiculo = Veiculo(0, self.capacidade)
        for i in range(1, len(rota) - 1):
            cliente = self.clientes[rota[i]]
            if(veiculo.carregando + cliente.demanda > veiculo.capacidade):
                return -1

            dist = self.matrizDistancia[rota[i - 1]][cliente.id]
            distDepot = self.matrizDistancia[cliente.id][self.deposito.id]

            if(veiculo.tempo + dist > cliente.terminoJanela):
                return -1

            if(veiculo.tempo + dist < cliente.inicioJanela):
                if(cliente.inicioJanela + cliente.tempoServico + distDepot > self.deposito.terminoJanela):
                    return -1
            else:
                if(veiculo.tempo + dist + cliente.tempoServico + distDepot > self.deposito.terminoJanela):
                    return -1
            veiculo.capacidade += cliente.demanda
            if(veiculo.tempo + dist < cliente.inicioJanela):
                veiculo.tempo = cliente.inicioJanela + cliente.tempoServico
            else:
                veiculo.tempo = veiculo.tempo + dist + cliente.tempoServico


    def OPT_2(self):
        veiculos = self.geraRota()
        for veiculo in veiculos:
            if(len(veiculo.rota) > 3):
                rotaFit = self.calculaFitnessRotaOnly(veiculo.rota)
                for i in range(len(veiculo.rota) - 1):
                    for j in range(i + 2, len(veiculo.rota) - 1):
                        self.posicao[veiculo.rota[i + 1] - 1], self.posicao[veiculo.rota[j] - 1] = self.posicao[veiculo.rota[j] - 1], self.posicao[veiculo.rota[i + 1] - 1]
                        veiculo.rota[i + 1], veiculo.rota[j] = veiculo.rota[j], veiculo.rota[i + 1]
                        fitness = self.violaRegraOnly(veiculo.rota)
                        if(fitness > 0 and fitness < rotaFit):
                            # print(rotaFit, fitness)
                            rotaFit = fitness
                        else:
                            self.posicao[veiculo.rota[i + 1] - 1], self.posicao[veiculo.rota[j] - 1] = self.posicao[veiculo.rota[j] - 1], self.posicao[veiculo.rota[i + 1] - 1]
                            veiculo.rota[i + 1], veiculo.rota[j] = veiculo.rota[j], veiculo.rota[i + 1]
