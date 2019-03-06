class Particle:
    def __init__(self, perc):
        import copy, random
        import Global
        import numpy as np

        self.w_i = 0.9
        self.w_f = 0.4
        self.w = self.w_i

        self.fator_Cognitivo = 2
        self.fator_Social = 2

        self.minPosCliente = -100000
        self.maxPosCliente = +100000
        self.minVelCliente = -100000
        self.maxVelCliente = +100000

        self.minPosVeiculo = -200
        self.maxPosVeiculo = 200
        self.minVelVeiculo = -10
        self.maxVelVeiculo = 10

        self.vel = np.array([random.uniform(self.minVelCliente, self.maxVelCliente) for _ in range(Global.num_Clientes)])
        for i in range(2 * Global.num_Veiculos):
            self.vel = np.append(self.vel, random.uniform(self.minVelVeiculo, self.maxVelVeiculo))
        self.conf = self.nova_Rota(Global.clientes, perc)

        self.pbest = copy.deepcopy(self.conf)
        self.gbest = None
    
    def nova_Rota(self, clientes, perc):
        from .Configuracao import Configuracao

        conf = Configuracao(self.minPosCliente, self.maxPosCliente,
                            self.minPosVeiculo, self.maxPosVeiculo, perc)
        
        return conf

    def set_GBest(self, gBest):
        self.gbest = gBest
    
    def ajusta_Velocidade(self):
        import Global

        for i in range(Global.num_Clientes):
            self.vel[i] = max(self.minVelCliente, min(self.maxVelCliente, self.vel[i]))
        
        for i in range(2 * Global.num_Veiculos):
            idx = Global.num_Clientes + i
            self.vel[idx] = max(self.minVelVeiculo, min(self.maxVelVeiculo, self.vel[idx]))

    def update_Velocidade(self, itera):
        import random, Global

        r1, r2 = random.uniform(0, 1), random.uniform(0, 1)
        self.vel =  self.w * self.vel + \
                    self.fator_Cognitivo * r1 * (self.pbest.conf - self.conf.conf) + \
                    self.fator_Social * r2 * (self.gbest.conf - self.conf.conf)

        self.w = self.w_f + (Global.NUM_ITERACOES - itera) * (
            self.w_i - self.w_f) / float(Global.NUM_ITERACOES)
        
        self.ajusta_Velocidade()

    def ajusta_Posicao(self):
        import Global

        for i in range(Global.num_Clientes):
            if(self.conf.conf[i] < self.minPosCliente):
                self.conf.conf[i] = self.minPosCliente
                self.vel[i] = 0
            elif(self.conf.conf[i] > self.maxPosCliente):
                self.conf.conf[i] = self.maxPosCliente
                self.vel[i] = 0                

        for i in range(2 * Global.num_Veiculos):
            idx = Global.num_Clientes + i
            if(self.conf.conf[idx] < self.minPosVeiculo):
                self.conf.conf[i] = self.minPosVeiculo
                self.vel[i] = 0
            elif(self.conf.conf[idx] > self.maxPosVeiculo):
                self.conf.conf[i] = self.maxPosVeiculo
                self.vel[i] = 0

            # self.conf.conf[idx] = max(self.minPosVeiculo, min(self.maxPosVeiculo, self.conf.conf[idx]))

    def update_Posicao(self):
        self.conf.conf += self.vel
        
        self.ajusta_Posicao()
    
    def update(self, perc):
        import copy

        self.conf.update(perc)
        if(self.conf.fitness < self.pbest.fitness):
            self.pbest = copy.deepcopy(self.conf)
            if(self.pbest.fitness < self.gbest.fitness):
                return True
        return False
