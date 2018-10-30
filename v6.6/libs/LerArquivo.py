class LerArquivo:
    def __init__(self):
        pass

    def readFile(self, file):
        arq = open(file)
        coords = []
        demandas = []
        coletas = []
        timeWindow = []
        veiculo_Capacidades = []
        # numVeiculos, capacidade = int(line.split()[0]), int(line.split()[1])
        # dados = line.split()
        # numVeiculos = int(dados[0])
        # qtd_Tipos = int(dados[1])
        # for k in range(1, 1 + qtd_Tipos):
        #     qtd, cap = int(dados[2 * k]), int(dados[2 * k + 1])
        #     for j in range(qtd):
                # veiculo_Capacidades.append(cap)
        for idx, line in enumerate(arq.readlines()):
            if(idx >= 1):
                line = [float(x) for x in line.split()]
                if(line == []): break
                coords.append((line[1], line[2]))
                demandas.append(line[7])
                coletas.append(line[6])
                timeWindow.append((line[3], line[4], line[5]))
            else:
                _, num_Clientes, num_Depositos, __ = map(int, line.split())

        matrizDistancia = [[0 for _ in range(num_Clientes + num_Depositos)] for _ in range(num_Clientes + num_Depositos)]

        def euclidianDistance(a, b):
            from math import sqrt
            return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        for i in range(num_Clientes + num_Depositos):
            for j in range(i + 1, num_Clientes + num_Depositos):
                matrizDistancia[i][j] = euclidianDistance(coords[i], coords[j])
                matrizDistancia[j][i] = matrizDistancia[i][j]

        arqVeiculos = open("In/In_Veiculos")
        for idx, line in enumerate(arqVeiculos.readlines()):
            if(idx == 0):
                numVeiculos = int(line)
            else:
                tmp = line.split()
                qtd, capacidade, custo = int(tmp[0]), int(tmp[1]), float(tmp[2])
                for i in range(qtd):
                    veiculo_Capacidades.append((capacidade, custo))
        tam_Veiculo_Capacidades = len(veiculo_Capacidades)
        for i in range(num_Depositos - 1):
            for j in range(tam_Veiculo_Capacidades):
                veiculo_Capacidades.append(veiculo_Capacidades[j])
        # print(veiculo_Capacidades)
        numVeiculos = numVeiculos * num_Depositos

        return numVeiculos, num_Depositos, num_Clientes, veiculo_Capacidades, coords, demandas, coletas, timeWindow, matrizDistancia
