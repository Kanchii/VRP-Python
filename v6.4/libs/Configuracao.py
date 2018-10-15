class Configuracao:
    def __init__(self, minPosCliente, maxPosCliente,
                 minPosVeiculo, maxPosVeiculo):
        
        import Global

        self.conf = self.nova_Conf(minPosCliente, maxPosCliente, minPosVeiculo, maxPosVeiculo)
        self.rotas = self.gera_Rotas_Ant()
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
            rotas[i].OPT_2()
        return rotas
    
    def gera_Rotas_Ant(self):
        import Global
        from .Veiculo import Veiculo
        rotas = []
        conf_Clientes = self.conf[:Global.num_Clientes]

        ordem_Clientes = []
        for i in range(Global.num_Clientes):
            ordem_Clientes.append((conf_Clientes[i], i))
        ordem_Clientes.sort(key = lambda x: x[0])

        veiculo_Atual = Veiculo(0)

        for i in range(Global.num_Clientes):
            indice_Cliente = ordem_Clientes[i][1]
            if(not veiculo_Atual.quebra_Regra(Global.clientes[indice_Cliente])):
                veiculo_Atual.add(Global.clientes[indice_Cliente])
            else:
                # print(veiculo_Atual.tempo_Total + Global.clientes[indice_Cliente].tempo_Servico, Global.clientes[indice_Cliente].termina)
                veiculo_Atual.add(Global.deposito)
                veiculo_Atual.OPT_2()
                rotas.append(veiculo_Atual)
                veiculo_Atual = Veiculo(i)
                veiculo_Atual.add(Global.clientes[indice_Cliente])
        veiculo_Atual.add(Global.deposito)
        veiculo_Atual.OPT_2()
        rotas.append(veiculo_Atual)

        return rotas

    def pega_Distancias(self, pos_Cliente, conf_Veiculos):
        import Global

        retorno = []
        for i in range(Global.num_Veiculos):
            dist = self.distancia(pos_Cliente, (conf_Veiculos[2 * i], conf_Veiculos[2 * i + 1]))
            retorno.append((dist, i))
        retorno.sort(key = lambda x: x[0])
        return retorno

    def gera_Rotas_Omir(self):
        import Global
        from .Veiculo import Veiculo

        conf_Clientes = self.conf[:Global.num_Clientes]
        conf_Veiculos = self.conf[Global.num_Clientes:]
        for i in range(Global.num_Veiculos):
            conf_Veiculos[2 * i] = Global.deposito.pos[0]
            conf_Veiculos[2 * i + 1] = Global.deposito.pos[1]
        # matriz_Prioridade = self.gera_Matriz_Prioridade(Global.clientes, conf_Veiculos)
        rotas = [Veiculo(i) for i in range(Global.num_Veiculos)]

        ordem_Clientes = []
        for i in range(Global.num_Clientes):
            ordem_Clientes.append((conf_Clientes[i], i))
        ordem_Clientes.sort(key=lambda x: x[0])

        for i in range(Global.num_Clientes):
            indice_Cliente = ordem_Clientes[i][1]
            distancias = self.pega_Distancias(Global.clientes[indice_Cliente].pos, conf_Veiculos)
            for j in range(Global.num_Veiculos):
                if(not rotas[distancias[j][1]].quebra_Regra(Global.clientes[indice_Cliente])):
                    rotas[distancias[j][1]].add(Global.clientes[indice_Cliente])
                    conf_Veiculos[2 * distancias[j][1]] = Global.clientes[indice_Cliente].pos[0]
                    conf_Veiculos[2 * distancias[j][1] + 1] = Global.clientes[indice_Cliente].pos[1]
                    break

        for i in range(Global.num_Veiculos):
            rotas[i].add(Global.deposito)
            rotas[i].OPT_2()
        return rotas

    def gera_Rotas_Artigo_Journal(self):
        import Global
        from .Veiculo import Veiculo

        conf_Clientes = self.conf[:Global.num_Clientes]
        conf_Veiculos = self.conf[Global.num_Clientes:]
        matriz_Prioridade = self.gera_Matriz_Prioridade(Global.clientes, conf_Veiculos)
        rotas = [Veiculo(i) for i in range(Global.num_Veiculos)]

        ordem_Clientes = []
        for i in range(Global.num_Clientes):
            ordem_Clientes.append((conf_Clientes[i], i))
        ordem_Clientes.sort(key=lambda x: x[0])

        for i in range(Global.num_Clientes):
            indice_Cliente = ordem_Clientes[i][1]
            for j in range(Global.num_Veiculos):
                indice_Veiculo = matriz_Prioridade[indice_Cliente][j]
                tmp = rotas[indice_Veiculo].quebra_Regra_Artigo(Global.clientes[indice_Cliente])
                if(tmp != -1):
                    rotas[indice_Veiculo].add_Artigo(Global.clientes[indice_Cliente], tmp)
                    rotas[indice_Veiculo].OPT_2()
                    break
        for i in range(Global.num_Veiculos):
            rotas[i].add(Global.deposito)
            # rotas[i].OPT_2()
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
        self.rotas = self.gera_Rotas_Artigo_Journal()
        self.fitness = self.calc_Fitness()
