class Particle:
    def __init__(self, capacidade_max, qtd_clientes, inercia = 1.0, fator_cognitivo = 0.6, fator_social = 0.4):
        from .funcoesGerais import geraEstado
        from copy import deepcopy

        self.qtd_clientes = qtd_clientes
        self.capacidade_max = capacidade_max
        self.inercia = inercia
        self.fator_cognitivo = fator_cognitivo
        self.fator_social = fator_social

        self.posicao = geraEstado(-5.0, 5.0, self.qtd_clientes)
        self.velocidade = geraEstado(-3.0, 3.0, self.qtd_clientes)

        self.pbest = deepcopy(self.posicao)
        self.pbest_fitness = int(1e9)

        self.gbest = deepcopy(self.posicao)

    def updateVelocidade(self):
        import random
        random_1 = random.random()
        random_2 = random.random()

        self.velocidade = self.inercia * self.velocidade\
                        + self.fator_cognitivo * random_1 * (self.pbest - self.posicao)\
                        + self.fator_social * random_2 * (self.gbest - self.posicao)

    def updatePosicao(self, matriz_distancias, demanda_clientes):
        self.posicao += self.velocidade
        fitness = self.calcFitness(matriz_distancias, demanda_clientes)
        if(fitness < self.pbest_fitness):
            self.pbest_fitness = fitness
            self.pbest = self.posicao

    def calcFitness(self, matriz_distancias, demanda_clientes):
        vet = []
        for i in range(self.qtd_clientes):
            vet.append((self.posicao[i], i))
        vet.sort(key = lambda x: x[0])
        fitness, qtd_atual = 0, 0
        seq = [0]
        for data in vet:
            if(data[0] + qtd_atual > self.capacidade_max):
                fitness += matriz_distancias[seq[-1]][0]
                seq = [0]
                qtd_atual = 0
            fitness += matriz_distancias[seq[-1]][data[1]]
            qtd_atual += demanda_clientes[data[1]]
            seq.append(data[1])
        fitness += matriz_distancias[seq[-1]][0]
        return fitness

    def OPT2(self, qtd, matriz_distancias, demanda_clientes):
        import random, copy
        cnt = 0
        while(cnt < qtd):
            f, s = random.randint(0, self.qtd_clientes - 1), random.randint(0, self.qtd_clientes - 1)
            self.posicao[f], self.posicao[s] = self.posicao[s], self.posicao[f]
            fit = self.calcFitness(matriz_distancias, demanda_clientes)
            if(fit < self.pbest_fitness):
                self.pbest = copy.deepcopy(self.posicao)
                self.pbest_fitness = fit
                cnt = 0
            else:
                self.posicao[f], self.posicao[s] = self.posicao[s], self.posicao[f]
                cnt += 1
