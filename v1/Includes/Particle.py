class Particle:
    def __init__(self, capacidade_max, qtd_clientes, inercia = 1, fator_cognitivo = 0.4, fator_social = 0.7):
        from .funcoesGerais import geraEstado
        from copy import deepcopy

        self.qtd_clientes = qtd_clientes
        self.capacidade_max = capacidade_max
        self.inercia = inercia
        self.fator_cognitivo = fator_cognitivo
        self.fator_social = fator_social

        self.posicao = geraEstado(-7.0, 7.0, self.qtd_clientes)
        self.velocidade = geraEstado(-3.0, 3.0, self.qtd_clientes)

        self.pbest = deepcopy(self.posicao)
        self.pbest_fitness = int(1e9)

        self.gbest = deepcopy(self.posicao)
        self.gbest_fitness = int(1e9)

    def updateVelocidade(self):
        import random, numpy as np
        random_1 = random.random()
        random_2 = random.random()

        self.velocidade = self.inercia * self.velocidade\
                        + self.fator_cognitivo * random_1 * (self.pbest - self.posicao)\
                        + self.fator_social * random_2 * (self.gbest - self.posicao)

        self.velocidade = np.clip(self.velocidade, -3, 3)
    def updatePosicao(self, matriz_distancias, demanda_clientes):
        from copy import deepcopy
        import numpy as np
        self.posicao += self.velocidade
        self.posicao = np.clip(self.posicao, -7, 7)
        fitness = self.calcFitness(matriz_distancias, demanda_clientes)
        if(fitness < self.pbest_fitness):
            self.pbest_fitness = fitness
            self.pbest = deepcopy(self.posicao)

    def calcFitness(self, matriz_distancias, demanda_clientes, posicao2 = None):
        vet = []
        if(posicao2 is None):
            for i in range(self.qtd_clientes):
                vet.append((self.posicao[i], i + 1))
        else:
            for i in range(self.qtd_clientes):
                vet.append((posicao2[i], i + 1))
        vet.sort(key = lambda x: x[0], reverse = True)
        fitness, qtd_atual = 0, 0
        seq = [0]
        for data in vet:
            if(demanda_clientes[data[1] - 1] + qtd_atual > self.capacidade_max):
                fitness += matriz_distancias[seq[-1]][0]
                seq = [0]
                qtd_atual = 0
            fitness += matriz_distancias[seq[-1]][data[1]]
            qtd_atual += demanda_clientes[data[1] - 1]
            seq.append(data[1])
        fitness += matriz_distancias[seq[-1]][0]
        return fitness

    def getRoutes(self, matriz_distancias, demanda_clientes):
        vet = []
        for i in range(self.qtd_clientes):
            vet.append((self.posicao[i], i + 1))
        vet.sort(key = lambda x: x[0], reverse = True)
        qtd_atual = 0
        seq = [0]
        routes = []
        for data in vet:
            if(demanda_clientes[data[1] - 1] + qtd_atual > self.capacidade_max):
                seq.append(0)
                routes.append(seq)
                seq = [0]
                qtd_atual = 0
            qtd_atual += demanda_clientes[data[1] - 1]
            seq.append(data[1])
        seq.append(0)
        routes.append(seq)
        return routes

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
                cnt += 1
                self.posicao[f], self.posicao[s] = self.posicao[s], self.posicao[f]
    def OPT2_(self, matriz_distancias, demanda_clientes):
        from copy import deepcopy
        import numpy as np
        flag = True
        while(flag):
            flag = False
            for i in range(len(self.posicao)):
                for j in range(i + 1, len(self.posicao)):
                    new_route = deepcopy(self.posicao[:i])
                    new_route = np.concatenate([new_route, self.posicao[i:j][::-1]])
                    new_route = np.concatenate([new_route, self.posicao[j:]])
                    fit = self.calcFitness(matriz_distancias, demanda_clientes, new_route)
                    if(fit < self.pbest_fitness):
                        self.pbest = deepcopy(new_route)
                        self.pbest_fitness = fit
                        flag = True

    def calcFitnessOneRoute(self, route, matriz_distancias):
        fit = 0
        for i in range(1, len(route)):
            fit += matriz_distancias[route[i - 1]][route[i]]
        return fit

    def OPT2_X(self, matriz_distancias, demanda_clientes, id, pos):
        import random, copy
        import networkx as nx
        import matplotlib.pyplot as plt

        flag = True
        routes = self.getRoutes(matriz_distancias, demanda_clientes)
        tot = 0
        for route in routes:
            actualFit = self.calcFitnessOneRoute(route, matriz_distancias)
            flag = True
            # if(id == 0):
            #     print(route)
            #     G = nx.Graph()
            #     G.add_node(0, pos = (pos[0][0], pos[0][1]))
            #     for i in range(1, len(route) - 1):
            #         G.add_node(route[i], pos = (pos[route[i]][0], pos[route[i]][1]))
            #     G.add_path(route)
            #     nx.draw(G, pos, with_labels = True)
            #     plt.show()
            while(flag):
                flag = False
                for i in range(len(route) - 1):
                    for j in range(i + 2, len(route) - 1):
                        if(i == j or j + 1 == i + 1): continue
                        route[i + 1], route[j] = route[j], route[i + 1]
                        fit = self.calcFitnessOneRoute(route, matriz_distancias)
                        if(fit < actualFit):
                            # print("Trocado {}-{} {}-{} por {}-{} {}-{}".format(route[i], route[j], route[i + 1], route[j + 1], route[i], route[i + 1], route[j], route[j + 1]))
                            actualFit = fit
                            self.posicao[route[i + 1] - 1], self.posicao[route[j] - 1] = self.posicao[route[j] - 1], self.posicao[route[i + 1] - 1]
                            flag = True
                        else:
                            route[i + 1], route[j] = route[j], route[i + 1]
            # if(id == 0):
            #     print(route)
            #     G = nx.Graph()
            #     G.add_node(0, pos = (pos[0][0], pos[0][1]))
            #     for i in range(1, len(route) - 1):
            #         G.add_node(route[i], pos = (pos[route[i]][0], pos[route[i]][1]))
            #     G.add_path(route)
            #     nx.draw(G, pos, with_labels = True)
            #     plt.show()
            tot += actualFit
        # print("Tot:", tot)
