class Rota:
    def __init__(self, capacidade_max, matriz_distancias, demanda_clientes, posicoes):
        self.capacidade_max = capacidade_max
        self.matriz_distancias = matriz_distancias
        self.demanda_clientes = demanda_clientes
        self.posicoes = posicoes

        self.routes = []
        self.psoRoute = self.newRandVector(-7, 7)
        self.fitness = 0
        self.geraRotas()

    def newRandVector(self, menor, maior):
        import numpy as np
        diff = maior - menor
        vet = np.random.random((1, len(self.demanda_clientes)))[0] * diff + menor
        return vet

    def geraRotas(self):
        vet = []
        for i in range(len(self.demanda_clientes)):
            vet.append((self.psoRoute[i], i + 1))
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
        self.fitness = fitness
        self.routes = routes

    def clipRoute(self, minimo, maximo):
        import numpy as np
        self.psoRoute = np.clip(self.psoRoute, minimo, maximo)

    def calcFitnessOneRoute(self, route):
        fit = 0
        for i in range(1, len(route)):
            fit += self.matriz_distancias[route[i - 1]][route[i]]
        return fit

    def OPT_Intra(self, id, pos):
        from copy import deepcopy as dp
        import networkx as nx
        import matplotlib.pyplot as plt

        for aux in self.routes:
            route = aux[0]
            # if(id == 0):
            #     print(route)
            #     G = nx.Graph()
            #     G.add_node(0, pos = (pos[0][0], pos[0][1]))
            #     for i in range(1, len(route) - 1):
            #         G.add_node(route[i], pos = (pos[route[i]][0], pos[route[i]][1]))
            #     G.add_path(route)
            #     nx.draw(G, pos, with_labels = True)
            #     plt.show()
            fit = self.calcFitnessOneRoute(route)
            flag = True
            while(flag):
                flag = False
                for i in range(len(route) - 1):
                    for j in range(i + 2, len(route) - 1):
                        if(i == j or j + 1 == i + 1): continue
                        route[i + 1], route[j] = route[j], route[i + 1]
                        tmp_fit = self.calcFitnessOneRoute(route)
                        if(tmp_fit < fit):
                            fit = tmp_fit
                            self.psoRoute[route[i + 1] - 1], self.psoRoute[route[j] - 1] = self.psoRoute[route[j] - 1], self.psoRoute[route[i + 1] - 1]
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

    def OPT_Inter(self, id, pos):
        n = len(self.routes)
        # print("Fitness agora: {}".format(self.fitness))
        for x in range(n):
            for y in range(x + 1, n):
                a = self.routes[x][0]
                capA = self.routes[x][1]
                b = self.routes[y][0]
                capB = self.routes[y][1]
                # if(id == 0):
                #     import networkx as nx
                #     import matplotlib.pyplot as plt
                #
                #     print("Routa A: {}".format(a))
                #     print("Routa B: {}".format(b))
                #
                #     G = nx.Graph()
                #     G.add_node(0, pos = (pos[0][0], pos[0][1]))
                #     for i in range(1, len(a) - 1):
                #         G.add_node(a[i], pos = (pos[a[i]][0], pos[a[i]][1]))
                #     for i in range(1, len(b) - 1):
                #         G.add_node(b[i], pos = (pos[b[i]][0], pos[b[i]][1]))
                #     G.add_path(a)
                #     G.add_path(b)
                #     nx.draw(G, pos, with_labels = True)
                #     plt.show()
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
                            if(fitAA + fitBB < fitA + fitB):
                                self.fitness = self.fitness + (fitAA + fitBB - (fitA +fitB))
                                a[i], b[j] = b[j], a[i]
                                self.psoRoute[a[i] - 1], self.psoRoute[b[j] - 1] = self.psoRoute[b[j] - 1], self.psoRoute[a[i] - 1]
                                a[i], b[j] = b[j], a[i]
                                self.routes[x] = (a, capA - dA + dB)
                                self.routes[y] = (b, capB - dB + dA)
                            else:
                                a[i], b[j] = b[j], a[i]
        #         if(id == 0):
        #             import networkx as nx
        #             import matplotlib.pyplot as plt
        #
        #             print("Routa A: {}".format(a))
        #             print("Routa B: {}".format(b))
        #
        #             G = nx.Graph()
        #             G.add_node(0, pos = (pos[0][0], pos[0][1]))
        #             for i in range(1, len(a) - 1):
        #                 G.add_node(a[i], pos = (pos[a[i]][0], pos[a[i]][1]))
        #             for i in range(1, len(b) - 1):
        #                 G.add_node(b[i], pos = (pos[b[i]][0], pos[b[i]][1]))
        #             G.add_path(a)
        #             G.add_path(b)
        #             nx.draw(G, pos, with_labels = True)
        #             plt.show()
        # print("Fitness Final: {}".format(self.fitness))
