from libs.LerArquivo import LerArquivo
from libs.Particle import Particle
from libs.Cliente import Cliente
from libs.Graph import Graph
import libs.Global as Global
import sys

GBEST = None

def get_GBest(particles):
    fitness = particles[0].pbest.fitness
    best = particles[0].pbest
    for particle in particles:
        if(particle.pbest.fitness < fitness):
            fitness = particle.pbest.fitness
            best = particle.pbest
    return best

def main():
    global NUM_PARTICLES, GBEST
    try:
        NUM_ITERACOES = 1000
        num_Clientes = 25 if (len(sys.argv) == 1) else int(sys.argv[1])
        NUM_PARTICLES = 100

        num_Veiculos, veiculos_Capacidades, coords, demandas, coletas, time_Window, matriz_Distancia = LerArquivo().readFile("In/TWSPD/{}C/IC102.txt".format(num_Clientes), num_Clientes)

        clientes = []
        for i in range(num_Clientes):
            clientes.append(Cliente(coords[i + 1], i + 1, demandas[i + 1], coletas[i + 1], time_Window[i + 1]))

        Global.init(num_Veiculos, num_Clientes, veiculos_Capacidades, coords, demandas, coletas, time_Window, matriz_Distancia, clientes, NUM_PARTICLES, NUM_ITERACOES)

        particles = []
        for i in range(Global.NUM_PARTICLES):
            particles.append(Particle())

        GBEST = get_GBest(particles)

        for i in range(Global.NUM_PARTICLES):
            particles[i].set_GBest(GBEST)
        
        print("Fitness atual: {}".format(GBEST.fitness))

        for itera in range(Global.NUM_ITERACOES):
            update = False
            for i in range(Global.NUM_PARTICLES):
                particles[i].update_Velocidade(itera)
                particles[i].update_Posicao()
                update = update or particles[i].update()
            if(update):
                GBEST = get_GBest(particles)
                for i in range(Global.NUM_PARTICLES):
                    particles[i].set_GBest(GBEST)
                print("Iteracao #{}".format(itera))
                print("Melhor fitness: {}".format(particles[0].gbest.fitness))
    finally:
        # for l in GBEST.rotas:
        #     print(' '.join([str(x.id) for x in l.clientes]))
        Graph().draw(GBEST.rotas)
if __name__ == "__main__":
    main()
