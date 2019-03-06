class Read_File():
    def __init__(self):
        pass
        # self.read_File(path_Clients, path_Vehicles)

    def read_File(self, path_Clients, path_Vehicles):
        from .Client import Client
        from .Vehicle import Vehicle

        clients = []
        with open(path_Clients) as clients_File:
            for i, line in enumerate(clients_File.readlines()):
                if(i == 0):
                    num_Clients = int(line.split()[1])
                else:
                    data = line.split()
                    '''
                         0 -> Index
                         1 -> X-position
                         2 -> Y-position
                         3 -> Start TW
                         4 -> End TW
                         5 -> Service time
                         6 -> Picking
                         7 -> Delivery
                    '''
                    client = Client(_id = i,
                                    _position=(float(data[1]), float(data[2])),
                                    _time_Window=(
                                        float(data[3]), float(data[4])),
                                    _service_Time=float(data[5]),
                                    _picking=float(data[6]),
                                    _delivery=float(data[7]))
                    clients.append(client)
        vehicles = []
        with open(path_Vehicles) as vehicles_File:
            for idx, line in enumerate(vehicles_File.readlines()):
                data = line.split()
                '''
                    0 -> Quantity
                    1 -> Capacity
                    2 -> Cost
                '''
                for i in range(int(data[0])):
                    vehicle = Vehicle(_id = idx,
                                      _capacity=float(data[1]),
                                      _cost=float(data[2]), _depot = clients[0])
                    vehicles.append(vehicle)

        return num_Clients, clients, vehicles
        
