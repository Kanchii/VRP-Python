def init(_num_Veiculos, _num_Clientes, _veiculos_Capacidades, _coords, _demandas, _coletas,
         _time_Window, _matriz_Distancia, _clientes, _NUM_PARTICLES, _NUM_ITERACOES):
    from .Cliente import Cliente

    global matriz_Distancia, clientes, veiculos_Capacidades, num_Veiculos, num_Clientes, deposito,\
           coords, demandas, coletas, time_Window, NUM_ITERACOES, NUM_PARTICLES

    deposito = Cliente(_coords[0], 0, _demandas[0], _coletas[0], _time_Window[0])
    matriz_Distancia = _matriz_Distancia
    clientes = _clientes
    veiculos_Capacidades = _veiculos_Capacidades
    num_Veiculos = _num_Veiculos
    num_Clientes = _num_Clientes
    coords = _coords
    demandas = _demandas
    coletas = _coletas
    time_Window = _time_Window
    NUM_PARTICLES = _NUM_PARTICLES
    NUM_ITERACOES = _NUM_ITERACOES
