class Graph:
    def __init__(self):
        pass

    def draw(self, veiculos, clientes, fitness = "Untitled"):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()

        for veiculo in veiculos:
            if(len(veiculo.rota) > 2):
                print(veiculo.rota)
                for indiceCliente in veiculo.rota:
                    G.add_node(indiceCliente, pos = clientes[indiceCliente].coord)
        for veiculo in veiculos:
            if(len(veiculo.rota) > 2):
                G.add_path(veiculo.rota)
        posicoes = []
        for cliente in clientes:
            posicoes.append(cliente.coord)
        nx.draw(G, posicoes, with_labels = True)
        plt.show()
