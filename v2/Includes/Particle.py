class Particle:
    def __init__(self, capacidade_max, matriz_distancias, demanda_clientes, posicoes):
        from .Rota import Rota
        from copy import deepcopy as dp

        self.posicao = Rota(capacidade_max, matriz_distancias, demanda_clientes, posicoes)
        self.velocidade = self.newRandVector(-5, 5, len(demanda_clientes))
        self.pbest = dp(self.posicao)
        # print(self.pbest.fitness, self.posicao.fitness)
        self.gbest = None

        self.fator_cognitivo = 0.4
        self.fator_social = 0.6
        self.w = 1.0

    def newRandVector(self, menor, maior, qtd):
        import numpy as np
        diff = maior - menor
        vet = np.random.random((1, qtd))[0] * diff + menor
        return vet

    def updateVelocidade(self):
        import random, numpy as np
        random_1 = random.random()
        random_2 = random.random()

        self.velocidade = self.w * self.velocidade\
                        + self.fator_cognitivo * random_1 * (self.pbest.psoRoute - self.posicao.psoRoute)\
                        + self.fator_social * random_2 * (self.gbest.psoRoute - self.posicao.psoRoute)
        self.velocidade = np.clip(self.velocidade, -5, 5)

    def updatePosicao(self):
        from copy import deepcopy as dp
        self.posicao.psoRoute += self.velocidade
        self.posicao.clipRoute(-7, 7)
        self.posicao.geraRotas()
        # if(self.posicao.fitness < self.pbest.fitness):
        #     print("oi")
        #     self.pbest = dp(self.posicao)

    def OPT_Intra(self, id, pos):
        self.posicao.OPT_Intra(id, pos)

    def OPT_Inter(self, id, pos):
        self.posicao.OPT_Inter(id, pos)

    def updatePBest(self):
        from copy import deepcopy as dp
        if(self.posicao.fitness < self.pbest.fitness):
            self.pbest = dp(self.posicao)
