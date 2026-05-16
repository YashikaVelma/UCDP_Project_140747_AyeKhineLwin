import numpy as np
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.operator.mutation import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations

class UCDPProblem(IntegerProblem):
    def __init__(self, num_locations, num_customers, fixed_costs, trans_matrix):
        super(UCDPProblem, self).__init__()
        self._number_of_variables = num_locations
        self._number_of_objectives = 1
        self._number_of_constraints = 0
        self._name = 'Uncapacitated Facility Location Problem'
        
        self.num_locations = num_locations
        self.num_customers = num_customers
        self.fixed_costs = fixed_costs
        self.trans_matrix = trans_matrix
        
        self.lower_bound = [0] * num_locations
        self.upper_bound = [1] * num_locations
        self.obj_directions = [self.MINIMIZE]

    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        opened_facilities = solution.variables
        if sum(opened_facilities) == 0:
            solution.objectives[0] = 9999999.0
            return solution
            
        total_fixed_cost = sum(np.array(self.fixed_costs) * np.array(opened_facilities))
        total_trans_cost = 0
        for c in range(self.num_customers):
            min_cost = float('inf')
            for f in range(self.num_locations):
                if opened_facilities[f] == 1 and self.trans_matrix[f][c] < min_cost:
                    min_cost = self.trans_matrix[f][c]
            total_trans_cost += min_cost
            
        solution.objectives[0] = float(total_fixed_cost + total_trans_cost)
        return solution

    def create_solution(self) -> IntegerSolution:
        new_solution = IntegerSolution(self.lower_bound, self.upper_bound, self.number_of_objectives, self.number_of_constraints)
        new_solution.variables = [np.random.randint(0, 2) for _ in range(self.number_of_variables)]
        return new_solution

    @property
    def number_of_variables(self) -> int: return self._number_of_variables
    @property
    def number_of_objectives(self) -> int: return self._number_of_objectives
    @property
    def number_of_constraints(self) -> int: return self._number_of_constraints
    @property
    def name(self) -> str: return self._name

def run_jmetal_optimization(num_locs, customer_count, fixed_costs, trans_matrix):
    problem = UCDPProblem(num_locs, customer_count, fixed_costs, trans_matrix)
    algorithm = GeneticAlgorithm(
        problem=problem,
        population_size=10,
        offspring_population_size=10,
        mutation=IntegerPolynomialMutation(probability=1.0 / num_locs),
        crossover=IntegerSBXCrossover(probability=0.9),
        termination_criterion=StoppingByEvaluations(max_evaluations=100)
    )
    algorithm.run()
    try:
        return algorithm.get_result()
    except AttributeError:
        return algorithm.solutions[0]
