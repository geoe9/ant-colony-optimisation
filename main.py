import re # regex used for reading file
import numpy as np # numpy used for array handling
from tqdm import tqdm # tqdm used for progress bar
import matplotlib.pyplot as plt # used to produce graphs from results

class AntColony:
    def __init__(self, number_of_ants: int, evaporation_rate: float, data: tuple[int, list[list[int], list[list[int]]]]) -> None:
        self.number_of_ants = number_of_ants
        self.evaporation_rate = evaporation_rate
        self.number_of_nodes, self.distance_matrix, self.flow_matrix = data

        # initalise pheromone matrix
        self.pheromone_matrix = [[np.random.random() if i != j else 0 for j in range(self.number_of_nodes + 1)] for i in range(self.number_of_nodes + 1)]
    
    def run(self, fitness_evaluations: int = 10_000) -> None:
        '''
        Runs the simulation until the provided number of fitness evaluations have been reached (default 10,000).
        '''
        # initalise all ants
        ants = [Ant(self) for _ in range(self.number_of_ants)]
        
        # initalise variables to store 'best' solution
        self.best_fitness = None
        best_path = None

        # initalise array to store results
        self.results = []
        
        # initalise progress bar to track simulations
        progress_bar = tqdm(range(fitness_evaluations), f'Running simulation (m={self.number_of_ants}, e={self.evaporation_rate})')

        ant_number = 0
        for i in progress_bar:
            path = ants[ant_number].calculatePath()
            fitness = ants[ant_number].calculatePathFitness()
            if self.best_fitness is None or fitness < self.best_fitness:
                self.best_fitness = fitness
                best_path = path
            self.results.append(fitness)
            
            # update pheromones when all ants have completed fitness evaluations
            if ant_number > self.number_of_ants - 2:
                for ant in ants:
                    ant.updatePheromones()
                ant_number = 0
                self.evaporatePheromones
            
            ant_number += 1

        # output results once simulation complete
        print(f'Simulation complete.\nBest fitness: {self.best_fitness:,d}\nPath: {best_path}\n')           
            
    def evaporatePheromones(self) -> None:
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

        # initialise allowed nodes matrix, start with all allowed apart from starting node
        self.allowed_nodes = [1 if i != 0 else 0 for i in range(self.colony.number_of_nodes + 1)]

        # iteratively choose next node to generate permutation
        self.path = []
        for i in range(self.colony.number_of_nodes):
            self.chooseNextNode()
        return self.path

    def chooseNextNode(self) -> None:
        '''
        Chooses next node randomly, with bias towards nodes with more pheromone.
        '''
        # calculate node weightings with current pheromone matrix, remove nodes that have already been visited
        next_node_weightings = np.multiply([i for i in self.colony.pheromone_matrix[self.current_node]], self.allowed_nodes)

        # convert weightings to probabilities
        next_node_probabilities = np.array(next_node_weightings) / np.sum(next_node_weightings)

        # choose next node randomly with bias based on probabilites
        next_node = np.random.choice(self.colony.number_of_nodes + 1, p = next_node_probabilities)

        # add chosen node to solution
        self.path.append(next_node)

        # remove node from allowed nodes as to not be visited again
        self.allowed_nodes[next_node] = 0

        # set current node to chosen node
        self.current_node = next_node

    def calculatePathFitness(self) -> float:
        '''
        Calculates the fitness of a generated permutation.
        Note that lower fitness is better in this case.
        '''
        self.fitness = 0
        
        # sum cost from each facility to every other facility to calculate fitness
        for i in range(len(self.path)):
            for j in range(len(self.path)):
                self.fitness += self.colony.distance_matrix[i][j] * self.colony.flow_matrix[self.path[i] - 1][self.path[j] - 1]
        return self.fitness

    def updatePheromones(self) -> None:
        '''
        Updates the global pheromone matrix with values proportionate to fitness of the ant's generated permutation.
        '''
        # calculate pheromone amount - less fitness is better
        pheromone_amount = 1 / self.fitness

        # add pheromone to pheromone matrix
        self.colony.pheromone_matrix[0][self.path[0]] += pheromone_amount
        for i in range(0, len(self.path) - 1):
            self.colony.pheromone_matrix[self.path[i]][self.path[i+1]] += pheromone_amount

class FileReader:
    '''
    Class to read input file.
    '''
    def __init__(self, file_path: str):
        with open(file_path) as f:
            file_contents = f.read().strip()

            # split values/matricies
            data = re.split('\n[ ]+\n', file_contents)

            # read number of facilities
            self.number_of_nodes = int(data[0])

            # read distance matrix
            self.distance_matrix = [[int(y) for y in x.split()] for x in data[1].split("\n")]

            # read flow matrix
            self.flow_matrix = [[int(y) for y in x.split()] for x in data[2].split("\n")]
    
    def getData(self) -> tuple[int, list[list[int]], list[list[int]]]:
        '''
        Returns all values and matrices in a tuple:\n
        (Number of nodes, Distance matrix, Flow matrix)
        '''
        return self.number_of_nodes, self.distance_matrix, self.flow_matrix

if __name__ == "__main__":
    # read file
    file_data = FileReader("uni50a.dat").getData()

    # list of simluations to run (m, e)
    tests = [(100, 0.9)]

    for test in tests:
        # run each simulation 5 times
        for i in range(5):
            colony = AntColony(test[0], test[1], file_data)
            colony.run()
            
            # plot results with matplotlib.pyplot
            figure = plt.figure()
            plt.plot(colony.results)
            plt.title(f'm = {test[0]}, e = {test[1]}')
            plt.suptitle(f'Best fitness: {colony.best_fitness:,d}')
            plt.xlabel("Iteration"); plt.ylabel("Fitness")
            figure.savefig(fname=f'results/m{test[0]}_e{test[1]}_{i}.png')