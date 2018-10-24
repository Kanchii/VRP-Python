class LerArquivo:
    def __init__(self):
        pass

    def readFile(self, file, numClientes):
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

        matrizDistancia = [[0 for _ in range(numClientes + 1)] for _ in range(numClientes + 1)]

        def euclidianDistance(a, b):
            from math import sqrt
            return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        for i in range(numClientes + 1):
            for j in range(i + 1, numClientes + 1):
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
        # print(veiculo_Capacidades)
        return numVeiculos, veiculo_Capacidades, coords, demandas, coletas, timeWindow, matrizDistancia
