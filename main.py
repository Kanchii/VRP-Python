from Includes.funcoesGerais import init_Instancia, printGraph
from Includes.Particle import Particle
from copy import deepcopy

''' Constantes '''
MAX_PARTICLES = 10

if __name__ == '__main__':
    capacidade_max, qtd_clientes, demanda_clientes, maxi_caminhoes, posicoes, matriz_distancias = init_Instancia("Entradas/entrada_2")
    particles = []

    for _ in range(MAX_PARTICLES):
        particles.append(Particle(capacidade_max, qtd_clientes))

    for k in range(50000):
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
        if(k and k % 100000 == 0):
            for i in range(MAX_PARTICLES):
                print("i: {} | {}".format(i + 1, particles[i].velocidade))
        if(k % 500 == 0):
           for i in range(MAX_PARTICLES):
               particles[i].OPT2_X(matriz_distancias, demanda_clientes)
               # particles[i].OPT2_X(matriz_distancias, demanda_clientes)
        if(k % 1000 == 0):
            print(k, bestFit)

    printGraph(posicoes, particles[0].gbest, qtd_clientes, demanda_clientes, capacidade_max)
