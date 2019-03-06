def _init(_num_Clients, _num_Vehicles, _number_Type_Vehicles, _vehicle_Each_Type_Model,
          _MAX_PARTICLES, _MAX_ITERATION, _clients, _vehicles):
    global num_Clients, num_Vehicles, number_Type_Vehicles, vehicle_Each_Type_Model, clients, vehicles
    global MAX_ITERATION, MAX_PARTICLES

    num_Clients = _num_Clients
    num_Vehicles = _num_Vehicles
    number_Type_Vehicles = _number_Type_Vehicles
    vehicle_Each_Type_Model = _vehicle_Each_Type_Model
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

def calc_Distance(A, B): #(x, y)
    import math

    return (math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2))