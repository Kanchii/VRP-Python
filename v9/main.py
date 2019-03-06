from libs.Particle import Particle
from libs.Read_File import Read_File
import libs.Global as Global

def update_GBest(particles):
    import copy
    bestParticle = particles[0]
    for i in range(len(particles)):
        if(particles[i].pbest.fitness < bestParticle.pbest.fitness):
            bestParticle = copy.deepcopy(particles[i])
    for i in range(len(particles)):
        particles[i].gbest = copy.deepcopy(bestParticle.pbest)

def main():
    try:
        num_Clients, num_Vehicles, clients, vehicles = Read_File().read_File("In/TWSPD/25C/IC101.txt", "In/In_Veiculos")

        Global._init(_num_Clients = num_Clients, _num_Vehicles = num_Vehicles, _MAX_PARTICLES = 100, _MAX_ITERATION = 1000, _clients = clients, _vehicles = vehicles)

        # print("oi1")
        particles = []
        for i in range(Global.MAX_PARTICLES):
            print("Criando Particula #{}".format(i + 1))
            particles.append(Particle())
        # particles = [Particle() for _ in range(Global.MAX_PARTICLES)]
        # print("oi2")
        update_GBest(particles)
        # print("oi3")
        for i in range(Global.MAX_ITERATION):
            # print("oi4")
            change = 0
            for j in range(len(particles)):
                # print("oi5")
                particles[j].update_Velocity(i)
                # print("oi6")
                particles[j].update_Position()
                # print("oi7")
                change |= particles[j].update()
            if(change):
                update_GBest(particles)
            print("Iteracao #{}: {} {}".format(i + 1, particles[0].gbest.fitness_No_Cost, particles[0].gbest.fitness))
    finally:
        particles[0].gbest.show_VRP()

if __name__ == "__main__":
    main()
