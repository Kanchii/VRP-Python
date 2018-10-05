from libs.LerArquivo import LerArquivo
from libs.Particle import Particle
from libs.Cliente import Cliente
from libs.Graph import Graph
import libs.Global as Global

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
        num_Clientes = 100

        NUM_PARTICLES = 100

        num_Veiculos, capacidade, coords, demandas, time_Window, matriz_Distancia = LerArquivo().readFile("In/TW/{}C/C101.txt".format(num_Clientes), num_Clientes)

        clientes = []
        for i in range(num_Clientes):
            clientes.append(Cliente(coords[i + 1], i + 1, demandas[i + 1], time_Window[i + 1]))

        Global.init(num_Veiculos, num_Clientes, capacidade, coords, demandas, time_Window, matriz_Distancia, clientes, NUM_PARTICLES, NUM_ITERACOES)

        particles = []
        for i in range(Global.NUM_PARTICLES):
            particles.append(Particle())

        GBEST = get_GBest(particles)

        for i in range(Global.NUM_PARTICLES):
            particles[i].set_GBest(GBEST)

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
        
        # for i, particle in enumerate(particles):
        #     vel_Veiculo = particle.vel[Global.num_Clientes:]
        #     print("Particle #{} = {}".format(i + 1, vel_Veiculo))
    finally:
        Graph().draw(GBEST.rotas)
if __name__ == "__main__":
    main()
