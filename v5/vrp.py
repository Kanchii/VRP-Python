from libs.LerArquivo import LerArquivo
from libs.Particula import Particula
from libs.Graph import Graph

MAX_ITERACOES = 1000
NUM_PARTICLES = 100

if __name__ == "__main__":
    import copy
    fuckingBestFit = 1e9
    veiculos = None
    numClientes, capacidade, coords, demandas, timeWindow, matrizDistancia = LerArquivo().readFile("In/TW/25C/C101.txt")
    particulas = [Particula(numClientes, capacidade, coords, demandas, timeWindow, matrizDistancia) for _ in range(NUM_PARTICLES)]
    try:
        codificacao = None
        for particula in particulas:
            if(particula.fitness < fuckingBestFit):
                fuckingBestFit = particula.fitness
                codificacao = copy.deepcopy(particula.posicao)
        for i in range(NUM_PARTICLES):
            particulas[i].gbest = copy.deepcopy(codificacao)
            particulas[i].fitness = fuckingBestFit
        # print(p.posicao - p.gbest)
        atualizou = False
        for iteracao in range(MAX_ITERACOES):
            # print("Iteracao #{}: {:.5f}".format(iteracao, particulas[0].fitness))
            atualizou = False
            for i in range(NUM_PARTICLES):
                fitness = particulas[i].calculaFitness()
                if(fitness < particulas[i].fitness):
                    particulas[i].fitness = fitness
                    particulas[i].pbest = copy.deepcopy(particulas[i].posicao)
                particulas[i].atualizaVelocidade(iteracao, MAX_ITERACOES)
                particulas[i].atualizaPosicao()
                particulas[i].OPT_2()
                if(particulas[i].fitness < fuckingBestFit):
                    fuckingBestFit = particulas[i].fitness
                    veiculos = particulas[i].geraRota()
                    codificacao = copy.deepcopy(particulas[i].posicao)
                    atualizou = True
            if(atualizou):
                for i in range(NUM_PARTICLES):
                    particulas[i].gbest = copy.deepcopy(codificacao)
                print("Iteracao #{}: {:.5f}".format(iteracao, fuckingBestFit))
    finally:
        Graph().draw(veiculos, particulas[0].clientes, fuckingBestFit)
    # vet1 = [1, 2, 3, 4, 10, 10, 20, 20, 30, 30, 40, 40]
    # p = Particula(numClientes, capacidade, coords, demandas, timeWindow, matrizDistancia)
    # antes = p.geraRota(vet1)
    # Graph().draw(antes, p.clientes)
    # vet1[0], vet1[2] = vet1[2], vet1[0]
    # depois = p.geraRota(vet1)
    # Graph().draw(depois, p.clientes)
