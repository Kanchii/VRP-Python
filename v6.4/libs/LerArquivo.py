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
        for idx, line in enumerate(arq.readlines()):
            if(idx == 4):
                numVeiculos, capacidade = int(line.split()[0]), int(line.split()[1])
                dados = line.split()
                numVeiculos = int(dados[0])
                qtd_Tipos = int(dados[1])
                for k in range(1, 1 + qtd_Tipos):
                    qtd, cap = int(dados[2 * k]), int(dados[2 * k + 1])
                    for j in range(qtd):
                        veiculo_Capacidades.append(cap)
            elif(idx >= 9):
                line = map(int, line.split())
                if(line == []): break
                coords.append((line[1], line[2]))
                demandas.append(line[3])
                coletas.append(line[4])
                timeWindow.append((line[5], line[6], line[7]))

        matrizDistancia = [[0 for _ in range(numClientes + 1)] for _ in range(numClientes + 1)]

        def euclidianDistance(a, b):
            from math import sqrt
            return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        for i in range(numClientes + 1):
            for j in range(i + 1, numClientes + 1):
                matrizDistancia[i][j] = euclidianDistance(coords[i], coords[j])
                matrizDistancia[j][i] = matrizDistancia[i][j]

        return numVeiculos, veiculo_Capacidades, coords, demandas, coletas, timeWindow, matrizDistancia
