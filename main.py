from Includes.funcoesGerais import init_Instancia
from Includes.Particle import Particle

''' Constantes '''
MAX_PARTICLES = 40

capacidade_max, qtd_clientes, demanda_clientes, maxi_caminhoes, posicoes, matriz_distancias = init_Instancia("Entradas/entrada_1")
particles = []

for _ in range(MAX_PARTICLES):
    particles.append(Particle(capacidade_max, qtd_clientes))

for _ in range(20):
    print(particles[0].velocidade[0])
    particles[0].updateVelocidade()
    particles[0].updatePosicao(matriz_distancias, demanda_clientes)
