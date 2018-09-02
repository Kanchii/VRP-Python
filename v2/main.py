from Includes.funcoesGerais import init_Instancia, printGraph
from Includes.Particle import Particle
from copy import deepcopy as dp

''' Constantes '''
MAX_PARTICLES = 10
MAX_ITERACAO = 100000

if __name__ == '__main__':
    capacidade_max, qtd_clientes, demanda_clientes, maxi_caminhoes, posicoes, matriz_distancias = init_Instancia("Entradas/entrada_1")

    particles = []
    for i in range(MAX_PARTICLES):
        particles.append(Particle(capacidade_max, matriz_distancias, demanda_clientes, posicoes))
    tmp = dp(particles[0].pbest)
    for i in range(MAX_PARTICLES):
        if(particles[i].pbest.fitness < tmp.fitness):
            tmp = dp(particles[i].pbest)
    for i in range(MAX_PARTICLES):
        particles[i].gbest = dp(tmp)

    # print("GBest comeco:", particles[0].gbest.fitness)

    for i in range(MAX_ITERACAO + 1):
        best = dp(particles[0].pbest)
        for j in range(MAX_PARTICLES):
            particles[j].updateVelocidade()
            particles[j].updatePosicao()

            # if(j == 0):
            #     print("Antes|\nPosicao: {}\nPBest: {}\n".format(particles[j].posicao.fitness, particles[j].pbest.fitness))
            #     printGraph(posicoes, qtd_clientes, particles[j].posicao.routes)

            # if(j == 0):
            #     print("Depois|\nPosicao: {}\nPBest: {}\n".format(particles[j].posicao.fitness, particles[j].pbest.fitness))
            #     printGraph(posicoes, qtd_clientes, particles[j].posicao.routes)
            particles[j].updatePBest()
        if(i % 50 == 0):
            for j in range(MAX_PARTICLES):
                particles[j].OPT_Inter(j, posicoes)
                particles[j].updatePBest()
        if(i % 100 == 0):
            for j in range(MAX_PARTICLES):
                particles[j].OPT_Intra(j, posicoes)
                particles[j].updatePBest()
        # if(i % 250 == 0):
        #     print("Iteracao #{} | Fitness: {}".format(i, particles[0].gbest.fitness))
        #     printGraph(posicoes, qtd_clientes, particles[0].gbest.routes)
        if(i % 250 == 0):
            print("Iteracao #{} | Fitness: {}".format(i, particles[0].gbest.fitness))
        for j in range(MAX_PARTICLES):
            if(particles[j].pbest.fitness < best.fitness):
                best = dp(particles[j].pbest)
        for j in range(MAX_PARTICLES):
            particles[j].gbest = dp(best)
    print("Iteracao #{} | Fitness: {}".format(i, particles[0].gbest.fitness))
    printGraph(posicoes, qtd_clientes, particles[0].gbest.routes)
