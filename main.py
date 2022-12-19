import re # regex used for reading file
import numpy as np # numpy used for array handling
from tqdm import tqdm # tqdm used for progress bar

class AntColony:
    def __init__(self, number_of_ants: int, evaporation_rate: float, data: tuple[int, list[list[int], list[list[int]]]]) -> None:
        self.number_of_ants = number_of_ants
        self.evaporation_rate = evaporation_rate
        self.number_of_nodes, self.distance_matrix, self.flow_matrix = data

        # initalise pheromone matrix
        self.pheromone_matrix = [[np.random.random() if i != j else 0 for j in range(self.number_of_nodes + 1)] for i in range(self.number_of_nodes + 1)]
    
    def run(self, iterations = 10_000):
        # initalise all ants
        ants = [Ant(self) for _ in range(self.number_of_ants)]
        
        # initalise variables to store 'best' solution
        best_fitness = None
        best_path = None
        
        progress_bar = tqdm(range(iterations))
        for i in progress_bar:
            for ant in ants:
                path = ant.calculatePath()
                fitness = ant.calculatePathFitness()
                if best_fitness is None or fitness < best_fitness:
                    best_fitness = fitness
                    best_path = path
            for ant in ants:
                ant.updatePheromones()
            self.evaporatePheromones()
            progress_bar.set_description(f'\rBest fitness:\t{best_fitness:,d}')
        print(f'\nSimulation complete.\nBest fitness: {best_fitness:,d}\nPath: {best_path}')
            
    def evaporatePheromones(self):
        '''
        Multiplies all values in the pheromone matrix by the evaporation rate to simulate pheromone evaporation/decay.
        '''
        self.pheromone_matrix = np.multiply(self.pheromone_matrix, self.evaporation_rate)

class Ant:
    def __init__(self, colony: AntColony):
        self.colony = colony

    def calculatePath(self) -> list:
        '''
        Generate a permutation.
        '''
        self.current_node = 0
        self.allowed_nodes = [1 if i != 0 else 0 for i in range(self.colony.number_of_nodes + 1)]
        self.path = []
        for i in range(self.colony.number_of_nodes):
            self.chooseNextNode()
        return self.path

    def chooseNextNode(self) -> None:
        '''
        Chooses next node randomly, with bias towards nodes with more pheromone.
        '''
        next_node_weightings = np.multiply([i for i in self.colony.pheromone_matrix[self.current_node]], self.allowed_nodes)
        next_node_probabilities = np.array(next_node_weightings) / np.sum(next_node_weightings)
        next_node = np.random.choice(self.colony.number_of_nodes + 1, p = next_node_probabilities)
        self.path.append(next_node)
        self.allowed_nodes[next_node] = 0
        self.current_node = next_node

    def calculatePathFitness(self) -> float:
        '''
        Calculates the fitness of a generated permutation.
        Note that lower fitness is better in this case.
        '''
        self.fitness = 0
        for i in range(len(self.path)):
            for j in range(len(self.path)):
                self.fitness += self.colony.distance_matrix[i][j] * self.colony.flow_matrix[self.path[i] - 1][self.path[j] - 1]
        return self.fitness

    def updatePheromones(self) -> None:
        '''
        Updates the global pheromone matrix with values proportionate to fitness of the ant's generated permutation.
        '''
        pheromone_amount = 1 / self.fitness
        self.colony.pheromone_matrix[0][self.path[0]] += pheromone_amount
        for i in range(0, len(self.path) - 1):
            self.colony.pheromone_matrix[self.path[i]][self.path[i+1]] += pheromone_amount
            self.colony.pheromone_matrix[self.path[i+1]][self.path[i]] += pheromone_amount

class FileReader:
    '''
    Class to read input file.
    '''
    def __init__(self, file_path: str):
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

file_data = FileReader("uni50a.dat").getData()
colony = AntColony(10, 0.9, file_data)
colony.run()