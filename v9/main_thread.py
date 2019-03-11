from libs.Particle import Particle
from libs.Read_File import Read_File
import libs.Global as Global
from math import ceil
import threading
import time

particles = [None] * 100

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


def update_GBest():
    import copy

    global particles

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

        threads_2 = []
        thread_1 = threading.Thread(target = initParticle, args = (0, 24,))
        thread_1.start()
        thread_2 = threading.Thread(target=initParticle, args=(25, 49,))
        thread_2.start()
        thread_3 = threading.Thread(target = initParticle, args = (50, 74,))
        thread_3.start()
        thread_4 = threading.Thread(target=initParticle, args=(75, 99,))
        thread_4.start()

        threads_2.append(thread_1)
        threads_2.append(thread_2)
        threads_2.append(thread_3)
        threads_2.append(thread_4)

        # for i in range(Global.MAX_PARTICLES):
        #     print("Criando Particula #{}".format(i + 1))
        #     particles.append(Particle())
        # for i in range(4):
        #     threads_2[i].start()
        for i in range(4):
            threads_2[i].join()

        update_GBest()
        for i in range(Global.MAX_ITERATION):
            time_start = time.time()
            threads = []
            thread_1 = threading.Thread(target=runParticle, args=(0, 24, i))
            thread_1.start()
            thread_2 = threading.Thread(target=runParticle, args=(25, 49, i))
            thread_2.start()
            thread_3 = threading.Thread(target=runParticle, args=(50, 74, i))
            thread_3.start()
            thread_4 = threading.Thread(target=runParticle, args=(75, 99, i))
            thread_4.start()

            threads.append(thread_1)
            threads.append(thread_2)
            threads.append(thread_3)
            threads.append(thread_4)
            # for i in range(4):
            #     threads[i].start()
            for j in range(4):
                threads[j].join()
            # change = 0
            # for j in range(len(particles)):
            #     particles[j].update_Velocity(i)
            #     particles[j].update_Position()
            #     change |= particles[j].update()
            update_GBest()
            time_end = time.time()
            print("Time elapsed: {}".format(time_end - time_start))
            print("Iteracao #{}: {} {}".format(i + 1, particles[0].gbest.fitness_No_Cost, particles[0].gbest.fitness))
            print("-"*25)
    finally:
        particles[0].gbest.show_VRP()

if __name__ == "__main__":
    main()
