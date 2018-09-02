from Includes.funcoesGerais import init_Instancia, printGraph
from Includes.Particle import Particle
from copy import deepcopy

''' Constantes '''
MAX_PARTICLES = 10

if __name__ == '__main__':
    capacidade_max, qtd_clientes, demanda_clientes, maxi_caminhoes, posicoes, matriz_distancias = init_Instancia("Entradas/entrada_1")
    particles = []

    for _ in range(MAX_PARTICLES):
        particles.append(Particle(capacidade_max, qtd_clientes))

    for k in range(300000):
        gbest = None
        bestFit = 1e9
        for i in range(MAX_PARTICLES):
            particles[i].updateVelocidade()
            particles[i].updatePosicao(matriz_distancias, demanda_clientes)
            if(bestFit > particles[i].pbest_fitness):
                bestFit = particles[i].pbest_fitness
                best = deepcopy(particles[i].pbest)
        if(not best is None):
            for i in range(MAX_PARTICLES):
                particles[i].gbest = deepcopy(best)
                particles[i].gbest_fitness = bestFit
        if(k % 500 == 0):
           for i in range(MAX_PARTICLES):
               particles[i].OPT2(100, matriz_distancias, demanda_clientes)
               particles[i].OPT2_X(matriz_distancias, demanda_clientes, i, posicoes)
        if(k % 1000 == 0):
            print(k, bestFit)

    for i in range(MAX_PARTICLES):
        particles[i].OPT2(30, matriz_distancias, demanda_clientes)
        particles[i].OPT2_X(matriz_distancias, demanda_clientes, i, posicoes)
    printGraph(posicoes, particles[0].gbest, qtd_clientes, demanda_clientes, capacidade_max)
