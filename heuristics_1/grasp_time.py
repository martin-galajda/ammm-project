import math
from construct import construct
from local_search import local_search
from cost_function import problem_cost_function
import sys
import numpy as np
import time

def check_if_solution_makes_sense(solution):
  sum_in_rows = solution['pt'].sum(axis = 1)
  if np.any(sum_in_rows > 1):
    print(solution)
    print("Local search wrong because row > 1(package assigned to more trucks)")
    sys.exit()
  if np.any(sum_in_rows == 0):
    print(solution)
    print("Local search wrong because row = 0(package assigned to zero trucks)")
    sys.exit()


def grasp_by_max_time(cost_function, alpha, greedy_loss_function, max_time_in_seconds, input, params_glf = None):
  best_cost_solution = math.inf
  best_solution = None

  print("Initiating GRASP with time constraint...")
  time_start = time.time()
  time_current = time_start
  k = 0

  while time_current - time_start <= max_time_in_seconds:
    k = k + 1
    feasible_solution = construct(greedy_loss_function, alpha, input, params_glf)

    cost_of_new_solution, best_solution_in_neighbourhood = local_search(cost_function, input, feasible_solution)

    if (cost_of_new_solution < best_cost_solution):
      best_solution = best_solution_in_neighbourhood
      best_cost_solution = cost_of_new_solution

    time_current = time.time()

  time_spent_computing = time_current - time_start


  return (best_solution, best_cost_solution, time_spent_computing, k)
