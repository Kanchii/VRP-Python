from Includes.funcoesGerais import init_Instancia, printGraph
from Includes.Particle import Particle
from copy import deepcopy as dp
import time

''' Constantes '''
MAX_PARTICLES = 20

if __name__ == '__main__':
    try:
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
        ant = -1
        i = 0
        start = time.time()
        time.clock()
        while(True):
            mudancaGBest = False
            for j in range(MAX_PARTICLES):
                particles[j].updateVelocidade()
                particles[j].updatePosicao()
                mudancaGBest = mudancaGBest or particles[j].updatePBest()
            if(i % 25 == 0):
                for j in range(MAX_PARTICLES):
                    particles[j].OPT_Pos_Inter(j, posicoes)
                    particles[j].OPT_Pos_Intra(j, posicoes)
                    particles[j].OPT_Pos_Rand(j, posicoes)
                    mudancaGBest = mudancaGBest or particles[j].updatePBest()

    		if(i % 500 == 0):
    			for j in range(MAX_PARTICLES):
    				mudancaGBest = mudancaGBest or particles[j].OPT_PBest_Intra(j, posicoes)
            		mudancaGBest = mudancaGBest or particles[j].OPT_PBest_Rand(j, posicoes)
                    # mudancaGBest = mudancaGBest or particles[j].updatePBest()

            if(i % 100 == 0):
                tempo = time.time() - start
                print("Iteracao #{} | Tempo: {:.5f}s | Fitness: {}".format(i, tempo, particles[0].gbest.fitness))
            # if(particles[0].gbest.fitness != ant):
            #     print("Iteracao #{} | Fitness: {}".format(i, particles[0].gbest.fitness))
            #     ant = particles[0].gbest.fitness
            #     printGraph(posicoes, qtd_clientes, particles[0].gbest.routes)
            if(mudancaGBest):
                best = dp(particles[0].pbest)
                for j in range(MAX_PARTICLES):
                    if(particles[j].pbest.fitness < best.fitness):
                        best = dp(particles[j].pbest)
                for j in range(MAX_PARTICLES):
                    particles[j].gbest = dp(best)
            i += 1
    except:
        print("Iteracao #{} | Tempo: {:.5f}s | Fitness: {}".format(i, tempo, particles[0].gbest.fitness))
        printGraph(posicoes, qtd_clientes, particles[0].gbest.routes)
