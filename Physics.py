from pygame.math import Vector2 as V2
from random import randint, choice, sample, uniform


BODY_DENSITY = 5.0
AGITATION_MAGNITUDE = 1

# Initial Values
FRICTION_COEFFICIENT = 0.1
REPULSION_COEFFICIENT = 0.1


class Body:
    def __init__(self, pos, mass, radius=None, color=None, label=None):
        self.mass = mass
        self.radius = radius if radius else (mass ** 0.5) / BODY_DENSITY
        self.color = (randint(127, 255), randint(127, 255), randint(127, 255))
        self.pos = V2(pos)
        self.vel = V2(0, 0)
        self.label = label
    
    def apply_impulse(self, force, duration):
        self.vel += force * duration / self.mass
    
    def update_position(self, timestep):
        self.pos += self.vel * timestep


class Spring:
    def __init__(self, endpoints, length, k, damping):
        self.endpoints = endpoints
        self.length = length
        self.k = k
        self.damping = damping


def projection(a, b):
    return b * (a.dot(b) / b.length_squared())


class System:
    @staticmethod
    def from_graph(graph, spring_length_function=lambda w: 1, k_function=lambda w: w):
        body_map = {v: Body((uniform(1, 7), uniform(1, 5)), 1, label=str(v)) for v in graph.vertices}
        bodies = list(body_map.values())
        springs = [
            Spring((body_map[e[0]], body_map[e[1]]), spring_length_function(e[2]), k_function(e[2]), 0.2)
            for e in graph.edges
        ]
        return System(bodies, springs)
    
    @staticmethod
    def random(num_bodies, num_springs, spring_length=1):
        num_springs = max(num_bodies, num_springs)
        bodies = [Body((uniform(1, 7), uniform(1, 5)), randint(1, 5)) for _ in range(num_bodies)]
        springs = [
            Spring((a, choice([b for b in bodies if a is not b])), spring_length, uniform(0.5, 5), 2.0)
            for a in bodies
        ] + [
            Spring(sample(bodies, 2), spring_length, uniform(0.5, 5), 2.0)
            for _ in range(num_springs - num_bodies)
        ]
        return System(bodies, springs)

    def __init__(self, bodies, springs):
        self.bodies = bodies
        self.springs = springs
        self.repulsion_coefficient = REPULSION_COEFFICIENT
        self.friction_coefficient = FRICTION_COEFFICIENT

    def agitate(self):
        n = len(self.bodies)
        forces = [V2(uniform(-1, 1), uniform(-1, 1)) * AGITATION_MAGNITUDE for _ in range(n)]
        # ensure total momentum remains zero
        total_force = V2(0, 0)
        for f in forces: total_force += f
        offset = total_force / n
        for f in forces: f -= offset
        for b, f in zip(self.bodies, forces):
            b.apply_impulse(f, 1)
    
    def step(self, timestep):
        for s in self.springs:
            a, b = s.endpoints
            disp = b.pos - a.pos
            stretch = disp.length() - s.length
            hookian_force = (b.pos - a.pos).normalize() * (stretch * s.k)
            damping_force = (projection(a.vel, disp) - projection(b.vel, disp)) * s.damping
            force = hookian_force - damping_force
            a.apply_impulse(force, timestep)
            b.apply_impulse(-force, timestep)
        
        # apply mutual repulsion
        for i in range(len(self.bodies) - 1):
            for j in range(i + 1, len(self.bodies)):
                a, b = self.bodies[i], self.bodies[j]
                disp = a.pos - b.pos
                force = disp * (1 / disp.length_squared()) * self.repulsion_coefficient
                a.apply_impulse(force, timestep)
                b.apply_impulse(-force, timestep)

        for b in self.bodies:
            friction = b.vel * b.mass * -self.friction_coefficient   # use b.vel.normalize() for absolute friction
            b.apply_impulse(friction, timestep)
            b.update_position(timestep)
    
