def init(_num_Veiculos, _num_Clientes, _num_Depositos, _veiculos_Capacidades, _coords, _demandas, _coletas,
         _time_Window, _matriz_Distancia, _clientes, _NUM_PARTICLES, _NUM_ITERACOES):
    from .Cliente import Cliente

    global matriz_Distancia, clientes, veiculos_Capacidades, num_Veiculos, num_Clientes, num_Depositos, depositos,\
           coords, demandas, coletas, time_Window, NUM_ITERACOES, NUM_PARTICLES

    depositos = [] # Cliente(_coords[0], 0, _demandas[0], _coletas[0], _time_Window[0])
    for i in range(_num_Depositos):
        depositos.append(Cliente(_coords[_num_Clientes + i], _num_Clientes + i, _demandas[_num_Clientes + i],
                                 _coletas[_num_Clientes + i], _time_Window[_num_Clientes + i]))
    matriz_Distancia = _matriz_Distancia
    clientes = _clientes
    veiculos_Capacidades = _veiculos_Capacidades
    num_Depositos = _num_Depositos
    num_Veiculos = _num_Veiculos
    num_Clientes = _num_Clientes
    coords = _coords
    demandas = _demandas
    coletas = _coletas
    time_Window = _time_Window
    NUM_PARTICLES = _NUM_PARTICLES
    NUM_ITERACOES = _NUM_ITERACOES
