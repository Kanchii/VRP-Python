class Configuracao:
    def __init__(self, minPosCliente, maxPosCliente,
                 minPosVeiculo, maxPosVeiculo):
        
        import Global

        self.conf = self.nova_Conf(minPosCliente, maxPosCliente, minPosVeiculo, maxPosVeiculo)
        self.rotas = self.gera_Rotas()
        self.fitness = self.calc_Fitness()
    
    def nova_Conf(self, minPosCliente, maxPosCliente,
                  minPosVeiculo, maxPosVeiculo):
        import random, Global, numpy as np

        conf = np.array([random.uniform(minPosCliente, maxPosCliente) for _ in range(Global.num_Clientes)])
        for i in range(2 * Global.num_Veiculos):
            conf = np.append(conf, random.uniform(minPosVeiculo, maxPosVeiculo))
        return conf
    
    def calc_Fitness(self):
        fitness = 0
        for rota in self.rotas:
            fitness += rota.fitness
        return fitness

    def gera_Rotas(self):
        import Global
        from .Veiculo import Veiculo

        conf_Clientes = self.conf[:Global.num_Clientes]
        conf_Veiculos = self.conf[Global.num_Clientes:]
        matriz_Prioridade = self.gera_Matriz_Prioridade(Global.clientes, conf_Veiculos)
        rotas = [Veiculo(i) for i in range(Global.num_Veiculos)]

        ordem_Clientes = []
        for i in range(Global.num_Clientes):
            ordem_Clientes.append((conf_Clientes[i], i))
        ordem_Clientes.sort(key = lambda x: x[0])

        for i in range(Global.num_Clientes):
            indice_Cliente = ordem_Clientes[i][1]
            for j in range(Global.num_Veiculos):
                indice_Veiculo = matriz_Prioridade[indice_Cliente][j]
                if(not rotas[indice_Veiculo].quebra_Regra(Global.clientes[indice_Cliente])):
                    rotas[indice_Veiculo].add(Global.clientes[indice_Cliente])
                    break
        for i in range(Global.num_Veiculos):
            rotas[i].add(Global.deposito)
        return rotas
    
    def distancia(self, ponto_A, ponto_B):
        import math

        return (math.sqrt(math.pow(ponto_A[0] - ponto_B[0], 2) + math.pow(ponto_A[1] - ponto_B[1], 2)))
    
    def gera_Matriz_Prioridade(self, clientes, conf_Veiculos):
        import Global

        matriz_Prioridade = [[] for i in range(Global.num_Clientes)]
        for i, cliente in enumerate(clientes):
            tmp = []
            for j in range(Global.num_Veiculos):
                pos_Veiculo = (conf_Veiculos[2 * j], conf_Veiculos[2 * j + 1])
                dist = self.distancia(cliente.pos, pos_Veiculo)
                tmp.append((dist, j))
            tmp.sort(key = lambda x: x[0])
            for key in tmp:
                matriz_Prioridade[i].append(key[1])
        return matriz_Prioridade
    
    def update(self):
        self.rotas = self.gera_Rotas()
        self.fitness = self.calc_Fitness()
