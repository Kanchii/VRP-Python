class Vehicle():
    def __init__(self, _capacity, _cost, _depot, _id):
        from . import Global

        self.id = _id
        self.capacity = _capacity
        self.route = [_depot, _depot]
        self.cost = _cost
        self.fitness = 0
        self.carrying = 0
    
    def get_Insertion_Cost(self, client, route, pos, _l_f, _l_if, tipo):
        alpha = 0.01
        beta = 0.95
        zr = self.cost
        gama = 1.0
        c_0i = self.calc_Distance(route[0], client)
        c_ij = self.calc_Distance(client, route[pos-1])
        c_if = self.calc_Distance(client, route[pos])
        c_fj = self.calc_Distance(route[pos-1], route[pos])
        l_f = _l_f
        l_if = _l_if

        # print("L_F:", l_f, "L_IF:", l_if)

        cost = (alpha * c_0i - beta * (c_ij + c_if - c_fj) * zr + (1 - beta) * (l_if - l_f) + tipo * 13) ** (gama)
        return cost

    def insertion_Cost_Client(self, client):
        import copy

        insertion_Cost = -2e9
        insertion_Pos  = -1

        route_Copy = copy.deepcopy(self.route)

        for i in range(1, len(route_Copy)):
            _, time_Window_Before = self.simulate(route_Copy, pos = i)
            # route_Copy = route_Copy[:i] + [client] + route_Copy[i:]
            self.carrying += client.delivery
            # print("Tentando inserir o cliente {} na posicao {}".format(client.id, i))
            fitness_New_Client, time_Window_After = self.simulate(route_Copy[:i] + [client] + route_Copy[i:], pos = (i+1))
            self.carrying -= client.delivery
            # route_Copy = route_Copy[:i] + route_Copy[i+1:]
            if(fitness_New_Client == -1):
                # print("Tentei inserir em {} e deu ruim".format(i))
                continue
            # cost = self.get_Insertion_Cost(client, route_Copy, i, time_Window_Before, time_Window_After)
            tipo = 1 if client.id >= 5 else 0
            print(client.id, tipo)
            cost = self.get_Insertion_Cost(client, route_Copy, i, time_Window_Before, time_Window_After, tipo)# (fitness_New_Client - self.fitness) * self.cost
            if(cost > insertion_Cost):
                insertion_Cost = cost
                insertion_Pos = i
        return insertion_Cost, insertion_Pos
    
    def add_Client(self, client, insertion_Position, insertion_Cost):
        self.route = self.route[:insertion_Position] + [client] + self.route[insertion_Position:]
        self.fitness, _ = self.simulate(self.route)
        self.carrying += client.delivery

    def reverse_Route(self, route, i, j):
        first = route[:i]
        second = route[i:j][::-1]
        third = route[j:]
        return (first + second + third)

    def _2OPT(self):
        import copy

        flag = True
        while(flag):
            flag = False
            for i in range(0, len(self.route) - 2):
                for j in range(i+2, len(self.route) - 1):
                    self.route[i + 1], self.route[j] = self.route[j], self.route[i + 1]
                    # print("ANTES:", self.print_Route(print_ID = 1))
                    # tmp = copy.deepcopy(self.route)
                    # tmp = self.reverse_Route(tmp, i, j)
                    # print("DEPOIS:", self.print_Route(tmp, print_ID = 1))
                    fit, _ = self.simulate(self.route)
                    if(fit != -1): print(fit, self.fitness)
                    if(fit >= 0 and fit < self.fitness):
                        # print("Serviu para alguma coisa")
                        # self.route = copy.deepcopy(tmp)
                        self.fitness = fit
                        flag = True
                    else:
                        self.route[i + 1], self.route[j] = self.route[j], self.route[i + 1]
                    #    self.route = self.route[:i] + \
                    #        self.route[i:j:-1] + self.route[j:]
    def _OR_OPT(self):
        flag = True

        while(flag):
            flag = False
            for i in range(1, len(self.route) - 3):
                for j in range(i+3, len(self.route) - 2):
                    self.route[i], self.route[i+1], self.route[i+2], self.route[j] = self.route[i + 2], self.route[j], self.route[i], self.route[i+1]
                    fit, _ = self.simulate(self.route)
                    # print(fit, self.fitness)
                    if(fit >= 0 and fit < self.fitness):
                        # print("Serviu para alguma coisa 2")
                        self.fitness = fit
                        flag = True
                    else:
                        self.route[i], self.route[i+1], self.route[i+2], self.route[j] = self.route[i +
                                                                                                    2], self.route[j], self.route[i], self.route[i+1]

    def calc_Distance(self, a, b):
        import math
        return math.sqrt((a.position[0] - b.position[0]) ** 2 + (a.position[1] - b.position[1]) ** 2)

    def simulate(self, clients, pos = -1):
        import copy

        carrying = copy.deepcopy(self.carrying)
        dead_Weight = 0
        time_Window = 0
        fitness = 0
        time_Window_Reached = -1
        for i in range(1, len(clients)):
            carrying = carrying - clients[i].delivery
            dead_Weight = dead_Weight + clients[i].picking
            if(carrying + dead_Weight > self.capacity):
                return -1, -1
            
            distance = self.calc_Distance(clients[i - 1], clients[i])
            if(time_Window + distance > clients[i].time_Window[1]):
                return -1, -1

            fitness += distance
            if(pos != -1 and i == pos):
                time_Window_Reached = time_Window + distance
            if(time_Window + distance < clients[i].time_Window[0]):
                time_Window = clients[i].time_Window[0] + clients[i].service_Time
            else:
                time_Window = time_Window + distance + clients[i].service_Time
            # print("Time_Window:", time_Window, "range:", i)
        # print("Carai homi!")
        return fitness, time_Window_Reached
    
    def print_Route(self, rota = -1, print_ID = 0):
        if(rota == -1):
            rota = self.route            
        res = ""
        for i in rota:
            if(print_ID == 1):
                res += str(i.id) + " "
            else:
                res += "(" + str(i.position[0]) + "," + str(i.position[1]) + ") "
        return res
