def eucDist(pos_1, pos_2):
    return (((pos_1[0] - pos_2[0])**2 + (pos_1[1] - pos_2[1])**2) ** (0.5))

def init_Instancia(path):
    arq = open(path, 'r')
    all_text = arq.readlines()

    capacidade_max = int(all_text.pop(0))
    qtd_clientes = int(all_text.pop(0))
    demanda_clientes = []
    clientes = all_text.pop(0).split()
    for demanda in clientes:
        demanda_clientes.append(int(demanda))
    maxi_caminhoes = int(all_text.pop(0))
    posicoes = []
    for _ in range(qtd_clientes + 1):
        posicoes.append([int(x) for x in all_text.pop(0).split()])

    matriz_distancias = [[0 for _ in range(qtd_clientes + 1)] for _ in range(qtd_clientes + 1)]
    for i in range(qtd_clientes + 1):
        for j in range(i + 1, qtd_clientes + 1):
            matriz_distancias[i][j] = eucDist(posicoes[i], posicoes[j])
            matriz_distancias[j][i] = matriz_distancias[i][j]

    return capacidade_max, qtd_clientes, demanda_clientes, maxi_caminhoes, posicoes, matriz_distancias

def geraEstado(menor, maior, qtd):
    import numpy as np
    diff = maior - menor
    vet = np.random.random((1, qtd))[0] * diff + menor
    return vet
