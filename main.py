import re

class AntColony:
    def __init__(self, number_of_ants: int, evaporation_rate: float, data: tuple[int, list[list[int], list[list[int]]]]) -> None:
        self.number_of_ants = number_of_ants
        self.evaporation_rate = evaporation_rate
        self.number_of_nodes, self.distance_matrix, self.flow_matrix = data

        # compute initial heuristic matrix
        self.heuristic_matrix = [[round(1 / self.distance_matrix[i][j], 4) if i != j else 0 for j in range(self.number_of_nodes)] for i in range(self.number_of_nodes)]
        # initalise pheromone matrix
        self.pheromone_matrix = [[1 for j in range(self.number_of_nodes)] for i in range(self.number_of_nodes)]
    
    def run(self):
        self.number_of_fitness_evaluations = 0
        if self.number_of_fitness_evaluations <= 10_000:
            # loop
            pass

class Ant:
    def __init__(self, colony: AntColony):
        self.colony = colony

class FileReader:
    '''
    Class to read input file.
    '''
    def __init__(self, file_path: str) -> None:
        with open(file_path) as f:
            file_contents = f.read().strip()
            data = re.split('\n[ ]+\n', file_contents)
            self.number_of_nodes = int(data[0])
            self.distance_matrix = [[int(y) for y in x.split()] for x in data[1].split("\n")]
            self.flow_matrix = [[int(y) for y in x.split()] for x in data[2].split("\n")]
    
    def getData(self) -> tuple[int, list[list[int]], list[list[int]]]:
        '''
        Returns all values and matrices in a tuple:\n
        (Number of nodes, Distance matrix, Flow matrix)
        '''
        return self.number_of_nodes, self.distance_matrix, self.flow_matrix