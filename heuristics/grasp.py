import math
from construct import construct
from local_search import local_search
from cost_function import problem_cost_function
import sys
import numpy as np

def grasp(cost_function, alpha, greedy_loss_function, max_iterations, input):
  best_cost_solution = math.inf
  best_solution = None

  for k in range(max_iterations):
    #print(f"Running {k} iteration: construct")
    feasible_solution = construct(greedy_loss_function, alpha, input)

    #print(f"Running {k} iteration: local_search")
    cost_of_new_solution, best_solution_in_neighbourhood = local_search(cost_function, input, feasible_solution)

    print(f"Cost of new solution: {cost_of_new_solution}")
    print(f"Highest load of new solution: {feasible_solution['highest_loaded_truck_load']}")

    sum_in_rows = best_solution_in_neighbourhood['pt'].sum(axis = 1)
    if np.any(sum_in_rows > 1):
      print(best_solution_in_neighbourhood)
      print("Local search fucked up for row > 1")
      sys.exit()
    if np.any(sum_in_rows == 0):
      print(best_solution_in_neighbourhood)
      print("Local search fucked up for row = 0")
      sys.exit()

    if (cost_of_new_solution < best_cost_solution):
      best_solution = best_solution_in_neighbourhood
      best_cost_solution = cost_of_new_solution

    print(f"Run {k} iteration!!!")

  return (best_solution, best_cost_solution)
