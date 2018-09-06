class Particle:
    def __init__(self, capacidade_max, matriz_distancias, demanda_clientes, posicoes):
        from .Rota import Rota
        from copy import deepcopy as dp

        self.posicao = Rota(capacidade_max, matriz_distancias, demanda_clientes, posicoes)
        self.velocidade = self.newRandVector(-100000, 100000, len(demanda_clientes))
        self.pbest = dp(self.posicao)
        # print(self.pbest.fitness, self.posicao.fitness)
        self.gbest = None

        self.fator_cognitivo = 1.5
        self.fator_social = 4.1 - self.fator_cognitivo
        self.w = 1.0

    def newRandVector(self, menor, maior, qtd):
        import numpy as np
        diff = maior - menor
        vet = np.random.random((1, qtd))[0] * diff + menor
        return vet

    def updateVelocidade(self):
        import random, numpy as np
        from math import sqrt

        random_1 = random.random()
        random_2 = random.random()

        phi = self.fator_social + self.fator_cognitivo
        K = 2 / abs(2 - phi - sqrt(phi**2 - 4 * phi))

        self.velocidade = K * (self.velocidade\
                        + self.fator_cognitivo * random_1 * (self.pbest.psoRoute - self.posicao.psoRoute)\
                        + self.fator_social * random_2 * (self.gbest.psoRoute - self.posicao.psoRoute))
        self.velocidade = np.clip(self.velocidade, -100000, 100000)

    def updatePosicao(self):
        from copy import deepcopy as dp
        self.posicao.psoRoute += self.velocidade
        self.posicao.clipRoute(-100000, 100000)
        self.posicao.geraRotas()
        # if(self.posicao.fitness < self.pbest.fitness):
        #     print("oi")
        #     self.pbest = dp(self.posicao)

    def OPT_Pos_Rand(self, id, pos, itera, totItera):
        self.posicao.OPT_Rand(id, pos, itera, totItera)

    def OPT_Pos_Intra(self, id, pos, itera, totItera):
        self.posicao.OPT_Intra(id, pos, itera, totItera)

    def OPT_Pos_Inter(self, id, pos, itera, totItera):
        self.posicao.OPT_Inter(id, pos, itera, totItera)

    def OPT_PBest_Rand(self, id, pos, itera, totItera):
        return self.pbest.OPT_Rand(id, pos, itera, totItera)

    def OPT_PBest_Intra(self, id, pos, itera, totItera):
        return self.pbest.OPT_Intra(id, pos, itera, totItera)

    def OPT_PBest_Inter(self, id, pos, itera, totItera):
        return self.pbest.OPT_Inter(id, pos, itera, totItera)

    def updatePBest(self):
        from copy import deepcopy as dp
        if(self.posicao.fitness < self.pbest.fitness):
            self.pbest = dp(self.posicao)
            if(self.pbest.fitness < self.gbest.fitness):
                return True
        return False
