from spike.life.individuals import Individual
class Board:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.matrix = [['' for _ in range(x)] for _ in range(y)]
        print(self.matrix)

    def put_individual(self,individual,x, y):
        self.matrix[x][y] = individual
        print(self.matrix)
        c : Individual = individual
        print(c.group)