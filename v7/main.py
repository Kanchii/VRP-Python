class Client:
    def __init__(self, _id, _x, _y, _sw, _fw, _st, _pick, _deliv):
        self.id = _id
        self.x = _x
        self.y = _y
        self.sw = _sw
        self.fw = _fw
        self.st = _st
        self.pick = _pick
        self.deliv = _deliv
    
    def __str__(self):
        return "ID: {} | X: {} | Y: {} | SW: {} | FW: {} | ST: {} | PICK: {} | DELIV: {}".format(self.id, self.x, self.y,\
                                                                                  self.sw, self.fw, self.st,\
                                                                                  self.pick, self.deliv)

if __name__ == '__main__':
    clients = []
    depots = []
    num_clients = 0
    num_depots = 0
    depot_max_cap = 1200
    with open('In/MDTWSPDH/lpr01') as arq:
        content = arq.readlines()
        for i, line in enumerate(content):
            line_splited = line.split()
            if(i == 0):
                _, num_clients, num_depots, _ = map(int, line_splited)
                # print(num_clients, num_depots)
            else:
                _id = int(line_splited[0])
                _x = float(line_splited[1])
                _y = float(line_splited[2])
                _sw = float(line_splited[3])
                _fw = float(line_splited[4])
                _st = float(line_splited[5])
                _pick = float(line_splited[6])
                _deliv = float(line_splited[7])
                if(i <= num_clients):
                    clients.append(Client(_id, _x, _y, _sw, _fw, _st, _pick, _deliv))
                else:
                    depots.append(Client(_id, _x, _y, _sw, _fw, _st, _pick, _deliv))
    depots_max_caps = [depot_max_cap] * num_depots
    matrix_clients_depot = [[None for _ in range(num_depots)] for _ in range(num_clients)]
    
    def euclidean_Distance(x0, y0, x1, y1):
        import math        
        return ((x0 - x1) ** 2 + (y0 - y1) ** 2)

    for i, client in enumerate(clients):
        for j, depot in enumerate(depots):
            dist = euclidean_Distance(client.x, client.y, depot.x, depot.y)
            matrix_clients_depot[i][j] = (dist, j)
        matrix_clients_depot[i].sort(key = lambda x: x[0])
    
    depots_clients = [[] for _ in range(num_depots)]

    for i in range(num_clients):
        demand = clients[i].deliv
        flag = False
        for j in range(num_depots):
            depot = matrix_clients_depot[i][j][1]
            if(depots_max_caps[depot] >= demand):
                depots_clients[depot].append(i)
                depots_max_caps[depot] -= demand
                flag = True
                break
    
    for i in range(num_depots):
        num_clients_depot = len(depots_clients[i])
        with open('entry-{}'.format(i), 'w') as arq:
            arq.write(str(num_clients_depot) + "\n")
            depot = depots[i]
            string = "{} {} {} {} {} {} {} {}\n".format(depot.id, depot.x, depot.y, depot.sw,
                                                        depot.fw, depot.st, depot.pick, depot.deliv)
            arq.write(string)
            for j in range(num_clients_depot):
                client = clients[depots_clients[i][j]]
                string = "{} {} {} {} {} {} {} {}\n".format(client.id, client.x, client.y, client.sw,\
                                                          client.fw, client.st, client.pick, client.deliv)
                arq.write(string)
