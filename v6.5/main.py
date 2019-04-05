from libs.LerArquivo import LerArquivo
from libs.Particle import Particle
from libs.Cliente import Cliente
from libs.Graph import Graph
import libs.Global as Global
import sys
import math

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
	NUM_ITERACOES = 1000
	num_Clientes = 100
	NUM_PARTICLES = 100

	pastas = ["C101_Het_FC_1.0", "C101_Het_FC_3.0", "C101_Het_FC_1.85", "C101_Het_FC_2.15"]
	valores = [(1.0, 3.0), (3.0, 1.0), (1.85, 2.15), (2.15, 1.85)]
	# try:
	for (pasta, valor) in zip(pastas, valores):
		for arq in range(0, 11):
			with open("{}/{}_{}.txt".format(pasta, pasta, arq), "w") as file:
				num_Veiculos, veiculos_Capacidades, coords, demandas, coletas, time_Window, matriz_Distancia = LerArquivo().readFile("In/TWSPD/{}C/IC101.txt".format(num_Clientes), num_Clientes)

				clientes = []
				for i in range(num_Clientes):
					clientes.append(Cliente(coords[i + 1], i + 1, demandas[i + 1], coletas[i + 1], time_Window[i + 1]))

				Global.init(num_Veiculos, num_Clientes, veiculos_Capacidades, coords, demandas, coletas, time_Window, matriz_Distancia, clientes, NUM_PARTICLES, NUM_ITERACOES)

				particles = []
				for i in range(Global.NUM_PARTICLES):
					particles.append(Particle(1.0, valor[0], valor[1]))

				GBEST = get_GBest(particles)

				for i in range(Global.NUM_PARTICLES):
					particles[i].set_GBest(GBEST)

				print("Fitness atual: {}".format(GBEST.fitness))
				anterior = -1
				contador = 0
				for itera in range(Global.NUM_ITERACOES):
					update = False
					for i in range(Global.NUM_PARTICLES):
						particles[i].update_Velocidade(itera)
						particles[i].update_Posicao()
						temp_inicial = 10.0
						temp_final = 0.0000001
						A = 1 / (float(NUM_ITERACOES)) * math.log(temp_inicial / temp_final)
						t_atual = temp_inicial * math.exp(-A * (itera + 1))
						mapeado = t_atual / 10.0
						# print(itera, mapeado)
						update = update or particles[i].update(-1)
					if(update):
						GBEST = get_GBest(particles)
						for i in range(Global.NUM_PARTICLES):
							particles[i].set_GBest(GBEST)
					qtd_Veiculos = sum([1 for x in GBEST.rotas if len(x.clientes) > 2])
					file.write(str(itera) + ":" + str(particles[0].gbest.fitness) + ":" + str(qtd_Veiculos) + "\n")
					print("Iteracao #{}: {} com {} veiculos".format(itera, particles[0].gbest.fitness, qtd_Veiculos))
					if(particles[0].gbest.fitness <= 829.0):
						break
					if(particles[0].gbest.fitness == anterior):
						contador += 1
						if(contador >= 200):
							particles = []
							contador = 0
							for i in range(Global.NUM_PARTICLES):
								particles.append(Particle(1.0))
							GBEST = get_GBest(particles)
							for i in range(Global.NUM_PARTICLES):
								particles[i].set_GBest(GBEST)
					else:
						contador = 0
					anterior = particles[0].gbest.fitness
				# print("Iteracao #{}".format(itera))
				# print("Melhor fitness: {}".format(particles[0].gbest.fitness))

	# finally:
	# 	for l in GBEST.rotas:
	# 		print(' '.join([str(x.id) for x in l.clientes]))
	# 	Graph().draw(GBEST.rotas)
if __name__ == "__main__":
    main()
