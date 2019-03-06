def _init(_num_Clients, _MAX_PARTICLES, _MAX_ITERATION, _clients, _vehicles):
    global num_Clients, clients, vehicles
    global MAX_ITERATION, MAX_PARTICLES

    num_Clients = _num_Clients
    clients = _clients
    vehicles = _vehicles

    # Constants
    MAX_ITERATION = _MAX_ITERATION
    MAX_PARTICLES = _MAX_PARTICLES

def multiply_Vector_Constant(c, vector):
    result = []
    for i in range(len(vector)):
        result.append(c * vector[i])
    return result

def add_Vector_Vector(vector_1, vector_2):
    result = []
    for (i, j) in zip(vector_1, vector_2):
        result.append(i + j)
    return result