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
            for i in range(1, len(path)):
                G.add_node(path[i - 1], path[i])
            # G.add_path(path, weight = 10)
        edges = G.edges()
        colors = [G[u][v]['color'] for u, v in edges]
        # nx.draw(G, pos = Global.coords, edges = edges, with_labels = True, edge_color = colors)
        # plt.show()
