class Particle():
    def __init__(self):
        from .State import State
        from . import Global
        import copy
        
        self.lower_Bound_Pos = -100000
        self.upper_Bound_Pos = 100000
        self.lower_Bound_Vel = -100000
        self.upper_Bound_Vel = 100000

        self.w   = 0.9
        self.w_i = 0.9
        self.w_f = 0.4
        self.c_1 = 2.0
        self.c_2 = 2.0

        self.position = State(self.lower_Bound_Pos, self.upper_Bound_Pos)
        self.velocity = [0] * (Global.num_Clients + Global.num_Vehicles)

        self.pbest = copy.deepcopy(self.position)
        self.gbest = None
    

    def update_Velocity(self, actual_Iteration):
        import random
        from . import Global

        self.w = self.w_f + (Global.MAX_ITERATION - actual_Iteration) * (self.w_i - self.w_f) / float(Global.MAX_ITERATION)
        r_1, r_2 = random.random(), random.random()

        inertia          = Global.multiply_Vector_Constant(self.w, self.velocity)
        cognitive_factor = Global.multiply_Vector_Constant(self.c_1 * r_1, self.pbest.subtract(self.position))
        social_factor    = Global.multiply_Vector_Constant(self.c_2 * r_2, self.gbest.subtract(self.position))

        self.velocity    = Global.add_Vector_Vector(inertia, Global.add_Vector_Vector(cognitive_factor, social_factor))
        for i in range(len(self.velocity)):
            if(self.velocity[i] < self.lower_Bound_Vel or self.velocity[i] > self.upper_Bound_Vel):
                self.velocity[i] = 0

    def update_Position(self):
        # self.position.update(self.velocity)
        self.position.add_Velocity(self.velocity)
        self.position.set_Limits(self.lower_Bound_Pos, self.upper_Bound_Pos)

    def update(self):
        import copy

        # print('oi1')
        fitness = self.position.update()
        # print("Fitness: {} | PBest: {}".format(fitness, self.pbest.fitness))
        if(fitness < self.pbest.fitness):
            self.pbest = copy.deepcopy(self.position)
            return 1
        # print('oi2')
        return 0
