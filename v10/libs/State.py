class State():    
    def __init__(self, lower_Bound, upper_Bound, lower_Bound_Vehicle, upper_Bound_Vehicle):
        import random
        from . import Global

        self.configuration = []
        self.fitness = 0
        self.fitness_No_Cost = 0

        for i in range(Global.num_Clients):
            self.configuration.append(random.random()*(2 * upper_Bound) + lower_Bound)
        for i in range(Global.num_Vehicles * 2):
            self.configuration.append(random.random()*(2 * upper_Bound_Vehicle) + lower_Bound_Vehicle)
        self.update()

    def subtract(self, other):
        result = []
        for (i, j) in zip(self.configuration, other.configuration):
            result.append(i - j)
        return result
    
    def add_Velocity(self, other):
        for i in range(len(other)):
            self.configuration[i] += other[i]
        
    def set_Limits(self, lower_Bound, upper_Bound, lower_Bound_Vehicle, upper_Bound_Vehicle):
        for i in range(len(self.configuration)):
            if(self.configuration[i] < lower_Bound):
                self.configuration[i] = lower_Bound
            elif(self.configuration[i] > upper_Bound):
                self.configuration[i] = upper_Bound
    
    def create_Vehicle_Matrix(self, vehicle_Pos):
        from . import Global
        import copy
        
        clients = copy.deepcopy(Global.clients)

        priority_Matrix = [[] for i in range(Global.num_Clients+1)]

        for idx_Client, client in enumerate(clients):
            best_Vehicle_Idx = -1
            best_Distance = 1e9
            vehicle_Priority = []
            for idx_Vehicle in range(len(vehicle_Pos) // 2):
                vehicle_Coord = (vehicle_Pos[2 * idx_Vehicle], vehicle_Pos[2 * idx_Vehicle + 1])
                # print(vehicle_Coord, client.position)
                distance = Global.calc_Distance(client.position, vehicle_Coord)
                vehicle_Priority.append((distance, idx_Vehicle))
                # if(distance < best_Distance):
                #     best_Distance = distance
                #     best_Vehicle_Idx = idx_Vehicle
            # sequence_Vehicles_Client.append(Global.vehicles[best_Vehicle_Idx].id)
            vehicle_Priority.sort(key = lambda x : x[0])
            priority_Matrix[idx_Client] = copy.deepcopy(vehicle_Priority)
        # print(sequence_Vehicles_Client)
        return priority_Matrix

    def update(self, only_Route = 0):
        import copy
        from . import Global

        actual_Configuration_Clients = copy.deepcopy(self.configuration[:Global.num_Clients])
        for i in range(Global.num_Clients):
            actual_Configuration_Clients[i] = (actual_Configuration_Clients[i], i + 1)
        actual_Configuration_Clients.sort()
        vehicles_Pos = copy.deepcopy(self.configuration[Global.num_Clients:])

        priority_Matrix = self.create_Vehicle_Matrix(vehicles_Pos)
        # print(sequence_Vehicles_Client)
        # vehicles_Model = copy.deepcopy(Global.vehicle_Each_Type_Model)
        # routes = []
        # for i in range(Global.number_Type_Vehicles):
        #     routes.append([copy.deepcopy(vehicles_Model[i])])
        # print(routes)

        vehicles = copy.deepcopy(Global.vehicles)

        if(only_Route == 0):
            self.fitness = 0
            self.fitness_No_Cost = 0

        for (_, client_Index) in actual_Configuration_Clients:
            client = Global.clients[client_Index]
            flag = False
            for (_, vehicle_Index) in priority_Matrix[client_Index]:
                insertion_Cost, insertion_Position = vehicles[vehicle_Index].insertion_Cost_Client(client)
                if(insertion_Cost < 1e9):
                    vehicles[vehicle_Index].add_Client(client, insertion_Position, insertion_Cost)
                    flag = True
                    break
            if(not flag):
                self.fitness += 1e9
                self.fitness_No_Cost += 1e9
            # vehicle_Type = sequence_Vehicles_Client[client_Index]
            # insertion_Cost, insertion_Position = routes[vehicle_Type][-1].insertion_Cost_Client(client)
            # if(insertion_Cost >= 1e9):
            #     routes[vehicle_Type].append(copy.deepcopy(vehicles_Model[vehicle_Type]))
            #     insertion_Cost, insertion_Position = routes[vehicle_Type][-1].insertion_Cost_Client(client)
            #     if(insertion_Cost >= 1e9):
            #         self.fitness += 1e9
            #     else:
            #         routes[vehicle_Type][-1].add_Client(client, insertion_Position, insertion_Cost)
            # else:
            #     routes[vehicle_Type][-1].add_Client(client, insertion_Position, insertion_Cost)
        
        if(only_Route == 0):
            for vehicle in vehicles:
                self.fitness += vehicle.fitness * vehicle.cost
                self.fitness_No_Cost += vehicle.fitness
            return self.fitness
        else:
            return vehicles
        
        # if(only_Route == 0):
        #     return 10
        # else:
        #     return []

        # vehicles = copy.deepcopy(Global.vehicles)
        # if(only_Route == 0):
        #     self.fitness = 0
        #     self.fitness_No_Cost = 0

        # for (_, client_index) in actual_configuration:
        #     client = Global.clients[client_index]

        #     best_choice = (-1, -1, 1e9)
        #     for i, vehicle in enumerate(vehicles):
        #         insertion_Cost, insertion_Position = vehicle.insertion_Cost_Client(client)
        #         # print(client_index, insertion_Cost)
        #         if(insertion_Cost < best_choice[2]):
        #             best_choice = (i, insertion_Position, insertion_Cost)
        #     if(best_choice[0] == -1):
        #         if(only_Route == 0):
        #             self.fitness += 1e9
        #             self.fitness_No_Cost += 1e9
        #     else:
        #         # print(client_index, best_choice[2])
        #         vehicles[best_choice[0]].add_Client(client, best_choice[1], best_choice[2])
        # if(only_Route == 0):
        #     for i, vehicle in enumerate(vehicles):
        #         self.fitness += vehicle.fitness
        #         self.fitness_No_Cost += vehicle.fitness * vehicle.cost
        #     return self.fitness
        # else:
        #     return vehicles
    
    def show_VRP(self):
        import networkx as nx
        import matplotlib.pyplot as plt
        from . import Global

        vehicles = self.update(only_Route = 1)

        G = nx.DiGraph()
        for vehicle in vehicles:
            path = []
            for clients in vehicle.route:
                G.add_node(clients.id)
                path.append(clients.id)
            color = None
            if(vehicle.id == 0):
                color = 'black'
            elif(vehicle.id == 1):
                color = 'red'
            elif(vehicle.id == 2):
                color = 'blue'
            elif(vehicle.id == 3):
                color = 'green'
            G.add_path(path, color = color)
        coords = [-1]
        for client in Global.clients:
            coords.append(client.position)
        edges = G.edges()
        colors = [G[u][v]['color'] for u, v in edges]
        nx.draw(G, pos = coords, with_labels=True, edge_color = colors)
        plt.show()
