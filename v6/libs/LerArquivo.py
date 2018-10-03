class LerArquivo:
    def __init__(self):
        pass

    def readFile(self, file, numClientes):
        arq = open(file)
        coords = []
        demandas = []
        timeWindow = []
        for idx, line in enumerate(arq.readlines()):
            if(idx == 4):
                numVeiculos, capacidade = int(line.split()[0]), int(line.split()[1])
            elif(idx >= 9):
                line = map(int, line.split())
                if(line == []): break
                coords.append((line[1], line[2]))
                demandas.append(line[3])
                timeWindow.append((line[4], line[5], line[6]))

        matrizDistancia = [[0 for _ in range(numClientes + 1)] for _ in range(numClientes + 1)]

        def euclidianDistance(a, b):
            from math import sqrt
            return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        for i in range(numClientes + 1):
            for j in range(i + 1, numClientes + 1):
                matrizDistancia[i][j] = euclidianDistance(coords[i], coords[j])
                matrizDistancia[j][i] = matrizDistancia[i][j]

        return numVeiculos, capacidade, coords, demandas, timeWindow, matrizDistancia
