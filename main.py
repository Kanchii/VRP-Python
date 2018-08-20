from Includes.funcoesGerais import init_Instancia
from Includes.Particle import Particle

''' Constantes '''
MAX_PARTICLES = 40

capacidade_max, qtd_clientes, demanda_clientes, maxi_caminhoes, posicoes, matriz_distancias = init_Instancia("Entradas/entrada_1")
particles = []

for _ in range(MAX_PARTICLES):
    particles.append(Particle(capacidade_max, qtd_clientes, 1.2, 1.5, 2.5))

for _ in range(10000):
    best = None
    bestFit = 1e9
    for i in range(MAX_PARTICLES):
        particles[i].updateVelocidade()
        particles[i].updatePosicao(matriz_distancias, demanda_clientes)
        if(bestFit > particles[i].pbest_fitness):
            bestFit = particles[i].pbest_fitness
            best = particles[i].pbest
    for i in range(MAX_PARTICLES):
        particles[i].gbest = best
    if(_ % 10 == 0):
        for i in range(MAX_PARTICLES):
            particles[i].OPT2(20, matriz_distancias, demanda_clientes)
    if(_ % 100 == 0):
        print(bestFit)
