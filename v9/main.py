from libs.Particle import Particle
from libs.Read_File import Read_File
import libs.Global as Global
from math import ceil
import threading
import time

# particles = [None] * 100

class myThread (threading.Thread):
    def __init__(self, threadID, start, end):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.start = start
        self.end = end

    def run(self):
        runParticle(self.start, self.end)


class myThread_2 (threading.Thread):
    def __init__(self, threadID, start, end):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.start = start
        self.end = end

    def run(self):
        initParticle(self.start, self.end)


def update_GBest(particles):
    import copy

    # global particles

    bestParticle = particles[0]
    for i in range(len(particles)):
        if(particles[i].pbest.fitness < bestParticle.pbest.fitness):
            bestParticle = copy.deepcopy(particles[i])
    for i in range(len(particles)):
        particles[i].gbest = copy.deepcopy(bestParticle.pbest)

def initParticle(start, end):
    global particles

    for i in range(start, end + 1):
        print("Criando particula #{}".format(i))
        particles[i] = Particle()

def runParticle(start, end, itera):
    global particles
    change = 0
    for i in range(start, end + 1):
        particles[i].update_Velocity(itera)
        particles[i].update_Position()
        change |= particles[i].update()
    return change

def main():
    try:
        num_Clients, num_Vehicles, clients, vehicles = Read_File().read_File("In/TWSPD/100C/IC101.txt", "In/In_Veiculos")

        Global._init(_num_Clients = num_Clients, _num_Vehicles = num_Vehicles, _MAX_PARTICLES = 100, _MAX_ITERATION = 1000, _clients = clients, _vehicles = vehicles)
        for t in range(5):
            anterior = -1
            contador = 0
            with open("IC_101_{}.txt".format(t + 1), "w") as file:
                particles = []

                for i in range(Global.MAX_PARTICLES):
                    particles.append(Particle())

                update_GBest(particles)
                for i in range(Global.MAX_ITERATION):
                    change = 0
                    for j in range(len(particles)):
                        particles[j].update_Velocity(i)
                        particles[j].update_Position()
                        change |= particles[j].update()
                    if(change):
                        update_GBest(particles)
                    print("Iteracao #{}: {}".format(i + 1, particles[0].gbest.fitness))
                    file.write("{}:{}\n".format(i + 1, particles[0].gbest.fitness))
                    if(particles[0].gbest.fitness <= 830.5):
                        break
                    if(particles[0].gbest.fitness == anterior):
                        contador += 1
                        if(contador >= 300):
                            break
                    else:
                        contador = 0
                    anterior = particles[0].gbest.fitness
    finally:
        pass
if __name__ == "__main__":
    main()
