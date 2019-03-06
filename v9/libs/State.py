class State():    
    def __init__(self, lower_Bound, upper_Bound):
        import random
        from . import Global

        self.configuration = []
        self.fitness = 0
        self.fitness_No_Cost = 0

        for i in range(Global.num_Clients + Global.num_Vehicles):
            self.configuration.append(random.random()*(2 * upper_Bound) + lower_Bound)
        self.update()

    def subtract(self, other):
        result = []
        for (i, j) in zip(self.configuration, other.configuration):
            result.append(i - j)
        return result
    
    def add_Velocity(self, other):
        for i in range(len(other)):
            self.configuration[i] += other[i]
        
    def set_Limits(self, lower_Bound, upper_Bound):
        for i in range(len(self.configuration)):
            if(self.configuration[i] < lower_Bound):
                self.configuration[i] = lower_Bound
            elif(self.configuration[i] > upper_Bound):
                self.configuration[i] = upper_Bound
    
    def update(self, only_Route = 0):
        import copy
        from . import Global

        actual_configuration_client = copy.deepcopy(self.configuration[:Global.num_Clients])
        actual_configuration_vehicle = copy.deepcopy(self.configuration[Global.num_Clients:])
        for i in range(len(actual_configuration_client)):
            actual_configuration_client[i] = (actual_configuration_client[i], i + 1)
        for i in range(len(actual_configuration_vehicle)):
            actual_configuration_vehicle[i] = (actual_configuration_vehicle[i], i)
        actual_configuration_client.sort()
        actual_configuration_vehicle.sort()
        
        vehicles = copy.deepcopy(Global.vehicles)
        if(only_Route == 0):
            self.fitness = 0
            self.fitness_No_Cost = 0

        for (_, client_index) in actual_configuration_client:
            client = Global.clients[client_index]

            best_choice = (-1, -1, 1e9)
            for (_, vehicle_index) in actual_configuration_vehicle:
                vehicle = vehicles[vehicle_index]
                insertion_Cost, insertion_Position = vehicle.insertion_Cost_Client(client)
                # print(client_index, insertion_Cost)
                if(insertion_Cost < best_choice[2]):
                    best_choice = (vehicle_index, insertion_Position, insertion_Cost)
            if(best_choice[0] == -1):
                if(only_Route == 0):
                    self.fitness += 1e9
                    self.fitness_No_Cost += 1e9
            else:
                # print(client_index, best_choice[2])
                vehicles[best_choice[0]].add_Client(client, best_choice[1], best_choice[2])
        if(only_Route == 0):
            # print("---" * 20)
            for i, vehicle in enumerate(vehicles):
                # vehicle._2OPT()
                # print("Vehicle #{}: {}".format(i, len(vehicle.route)))
                # print("Route: {}".format(vehicle.print_Route()))
                # print("Fitness: {}".format(vehicle.fitness))
                self.fitness += vehicle.fitness * vehicle.cost
                self.fitness_No_Cost += vehicle.fitness
                # if(vehicle.fitness > 0):
                #     print(i, vehicle.fitness)
            return self.fitness
        else:
            return vehicles
    
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
            elif(vehicle.id == 4):
                color = 'orange'
            elif(vehicle.id == 5):
                color = 'pink'
            G.add_path(path, color = color)
        coords = [-1]
        for client in Global.clients:
            coords.append(client.position)
        edges = G.edges()
        colors = [G[u][v]['color'] for u, v in edges]
        nx.draw(G, pos = coords, with_labels=True, edge_color = colors)
        plt.show()
