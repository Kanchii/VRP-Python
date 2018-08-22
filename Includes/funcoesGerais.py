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

def printGraph(posicao, gbest, qtd_clientes, demanda_clientes, capacidade_max):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    for i in range(qtd_clientes + 1):
        G.add_node(i, pos = (posicao[i][0], posicao[i][1]))
    vet = []
    for i in range(qtd_clientes):
        vet.append((gbest[i], i + 1))
    vet.sort(key = lambda x: x[0], reverse = True)
    qtd_atual = 0
    seq = [0]
    idx = 1
    for data in vet:
        if(demanda_clientes[data[1] - 1] + qtd_atual > capacidade_max):
            seq.append(0)
            print("Rota #{}: {}".format(idx, seq))
            idx += 1
            G.add_path(seq)
            seq = [0]
            qtd_atual = 0
        qtd_atual += demanda_clientes[data[1] - 1]
        seq.append(data[1])
    seq.append(0)
    print("Rota #{}: {}".format(idx, seq))
    G.add_path(seq)
    nx.draw(G, posicao, with_labels = True)
    plt.show()
