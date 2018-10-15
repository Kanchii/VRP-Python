class Graph:
    def __init__(self):
        pass

    def draw(self, rotas):
        import Global
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()

        for rota in rotas:
            posicoes = []
            path = []
            for cliente in rota.clientes:
                path.append(cliente.id)
                G.add_node(cliente.id, pos = cliente.pos)
            # print(path)
            G.add_path(path)
        nx.draw(G, Global.coords, with_labels = True)
        plt.show()
