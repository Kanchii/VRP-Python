class Rota:
    def __init__(self, capacidade_max, matriz_distancias, demanda_clientes, posicoes):
        self.capacidade_max = capacidade_max
        self.matriz_distancias = matriz_distancias
        self.demanda_clientes = demanda_clientes
        self.posicoes = posicoes

        self.routes = []
        self.psoRoute = self.newRandVector(-100000, 100000)
        self.fitness = 0
        self.geraRotas()

    def newRandVector(self, menor, maior):
        import numpy as np
        diff = maior - menor
        vet = np.random.random((1, len(self.demanda_clientes)))[0] * diff + menor
        return vet

    def geraRotas(self, route = None):
        vet = []
        if(route is None):
            for i in range(len(self.demanda_clientes)):
                vet.append((self.psoRoute[i], i + 1))
        else:
            for i in range(len(self.demanda_clientes)):
                vet.append((route[i], i + 1))
        vet.sort(key = lambda x: x[0], reverse = True)
        fitness, qtd_atual = 0, 0
        seq = [0]
        routes = []
        for data in vet:
            if(self.demanda_clientes[data[1] - 1] + qtd_atual > self.capacidade_max):
                fitness += self.matriz_distancias[seq[-1]][0]
                seq.append(0)
                routes.append((seq, qtd_atual))
                seq = [0]
                qtd_atual = 0
            fitness += self.matriz_distancias[seq[-1]][data[1]]
            qtd_atual += self.demanda_clientes[data[1] - 1]
            seq.append(data[1])
        fitness += self.matriz_distancias[seq[-1]][0]
        seq.append(0)
        routes.append((seq, qtd_atual))
        if(route is None):
            self.fitness = fitness
            self.routes = routes
        else:
            return (fitness, routes)
    def clipRoute(self, minimo, maximo):
        import numpy as np
        self.psoRoute = np.clip(self.psoRoute, minimo, maximo)

    def calcFitnessOneRoute(self, route):
        fit = 0
        for i in range(1, len(route)):
            fit += self.matriz_distancias[route[i - 1]][route[i]]
        return fit

    # def calcFitnessPsoRoute(self, route):
    #     vet = []
    #     for i in range(len(self.demanda_clientes)):
    #         vet.append((route[i], i + 1))
    #     vet.sort(key = lambda x: x[0], reverse = True)
    #     fitness, qtd_atual = 0, 0
    #     seq = [0]
    #     routes = []
    #     for data in vet:
    #         if(self.demanda_clientes[data[1] - 1] + qtd_atual > self.capacidade_max):
    #             fitness += self.matriz_distancias[seq[-1]][0]
    #             seq.append(0)
    #             routes.append((seq, qtd_atual))
    #             seq = [0]
    #             qtd_atual = 0
    #         fitness += self.matriz_distancias[seq[-1]][data[1]]
    #         qtd_atual += self.demanda_clientes[data[1] - 1]
    #         seq.append(data[1])
    #     fitness += self.matriz_distancias[seq[-1]][0]
    #     seq.append(0)
    #     routes.append((seq, qtd_atual))
    #     return (fitness, routes)

    def OPT_Rand(self, id, pos, itera = -1, totItera = -1):
        import random
        from copy import deepcopy as dp
        cnt = 0
        tmp = dp(self.psoRoute)
        flag = False
        prob = itera / float(totItera)
        while(cnt < 100):
            s, f = random.randint(0, len(tmp) - 1), random.randint(0, len(tmp) - 1)
            tmp[s], tmp[f] = tmp[f], tmp[s]
            fitNewRoute, routesNewRoute = self.geraRotas(tmp)
            if(itera != -1):
                aux = random.uniform(0, 1)
                flag2 = aux > prob
            else:
                flag2 = False
            if(flag2 or fitNewRoute < self.fitness):
                # self.psoRoute = dp(tmp)
                self.fitness = fitNewRoute
                # self.routes = dp(routesNewRoute)
                flag = True
                cnt += 1
            else:
                tmp[s], tmp[f] = tmp[f], tmp[s]
                cnt += 1
        if(flag):
            self.psoRoute = dp(tmp)
            # fitNewRoute, routesNewRoute = self.calcFitnessPsoRoute(tmp)
            # self.fitness = fitNewRoute
            self.fitness, self.routes = self.geraRotas(tmp)
        return flag

    def OPT_Intra(self, id, pos, itera = -1, totItera = -1):
        import random
        from copy import deepcopy as dp
        import networkx as nx
        import matplotlib.pyplot as plt

        ultraFlag = False
        prob = itera / float(totItera)
        for aux in self.routes:
            route = aux[0]
            fit = self.calcFitnessOneRoute(route)
            flag = True
            while(flag):
                flag = False
                for i in range(len(route) - 1):
                    for j in range(i + 2, len(route) - 1):
                        if(i == j or j + 1 == i + 1): continue
                        route[i + 1], route[j] = route[j], route[i + 1]
                        tmp_fit = self.calcFitnessOneRoute(route)
                        if(itera != -1):
                            tmp = random.uniform(0, 1)
                            flag2 = tmp > prob
                        else:
                            flag2 = False
                        if(flag2 or tmp_fit < fit):
                            flag = True
                            fit = tmp_fit
                            self.psoRoute[route[i + 1] - 1], self.psoRoute[route[j] - 1] = self.psoRoute[route[j] - 1], self.psoRoute[route[i + 1] - 1]
                            ultraFlag = True
                        else:
                            route[i + 1], route[j] = route[j], route[i + 1]
        return ultraFlag

    def OPT_Inter(self, id, pos, itera = -1, totItera = -1):
        import random
        from copy import deepcopy as dp
        import networkx as nx
        import matplotlib.pyplot as plt

        n = len(self.routes)
        # print("Fitness agora: {}".format(self.fitness))
        flag = True
        ultraFlag = False
        prob = itera / float(totItera)
        while(flag):
            flag = False
            for x in range(n):
                for y in range(x + 1, n):
                    if(x == y): continue
                    a = dp(self.routes[x][0])
                    capA = self.routes[x][1]
                    b = dp(self.routes[y][0])
                    capB = self.routes[y][1]
                    for i in range(1, len(a) - 1):
                        dA = self.demanda_clientes[a[i] - 1]
                        for j in range(1, len(b) - 1):
                            dB = self.demanda_clientes[b[j] - 1]
                            if(capA - dA + dB <= self.capacidade_max and capB - dB + dA <= self.capacidade_max):
                                fitA = self.calcFitnessOneRoute(a)
                                fitB = self.calcFitnessOneRoute(b)
                                a[i], b[j] = b[j], a[i]
                                fitAA = self.calcFitnessOneRoute(a)
                                fitBB = self.calcFitnessOneRoute(b)
                                if(itera != -1):
                                    tmp = random.uniform(0, 1)
                                    flag2 = tmp > prob
                                else:
                                    flag2 = False
                                if(flag2 or fitAA + fitBB < fitA + fitB):
                                    self.fitness = self.fitness - ((fitA + fitB) - (fitAA + fitBB))
                                    self.psoRoute[a[i] - 1], self.psoRoute[b[j] - 1] = self.psoRoute[b[j] - 1], self.psoRoute[a[i] - 1]
                                    capA = capA - dA + dB
                                    capB = capB - dB + dA
                                    self.routes[x] = (a, capA)
                                    self.routes[y] = (b, capB)
                                    flag = True
                                    ultraFlag = True
                                else:
                                    a[i], b[j] = b[j], a[i]
        return ultraFlag
