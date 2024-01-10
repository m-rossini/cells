from spike.life.individuals import Individual
from spike.world.world_specs import Board

c1=Individual(1)
print(c1)

b=Board(3,5)
print(b)

b.put_individual(c1,1,2)