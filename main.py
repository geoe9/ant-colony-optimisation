class AntColony:
    def __init__(self, number_of_ants: int, evaporation_rate: float, data: list):
        self.number_of_ants = number_of_ants
        self.evaporation_rate = evaporation_rate
        self.data = data