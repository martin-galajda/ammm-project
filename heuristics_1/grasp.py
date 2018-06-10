import math
from construct import construct
from local_search import local_search
from cost_function import problem_cost_function
import sys
import numpy as np
import time 

def grasp(cost_function, alpha, greedy_cost_function, max_iterations, input):
  best_cost_solution = math.inf
  best_solution = None

  print("Initiating GRASP...")

  start = time.time()

  for k in range(max_iterations):
    feasible_solution = construct(greedy_cost_function, alpha, input)
    cost_of_new_solution, best_solution_in_neighbourhood = local_search(cost_function, input, feasible_solution)

    print(f"Cost of new solution: {cost_of_new_solution}")
    print(f"Highest load of new solution: {best_solution_in_neighbourhood['highest_loaded_truck_load']}")

    if (cost_of_new_solution < best_cost_solution):
      best_solution = best_solution_in_neighbourhood
      best_cost_solution = cost_of_new_solution

    

  return (best_solution, best_cost_solution, time.time() - start, max_iterations)
