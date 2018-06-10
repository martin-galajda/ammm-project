import math
import json
import pprint
import numpy as np
import json
import time, threading


from visualize_solution import visualize_solution
from grasp import grasp
from cost_function import problem_cost_function
from greedy_cost_function import greedy_cost_function
from grasp_time import grasp_by_max_time

# with open('latest_solution.json', 'w') as fp:
#   json.dump(best_solution, fp, sort_keys=True, indent=4)

def quit_computing(data):
  data["quit_computing"] = True

def run_experiment(input_filename, alpha = 0.8, max_iterations = 1000, max_time_in_seconds = None):
  with open(input_filename) as file_handle:
    data = json.loads(file_handle.read())

  data["stop_after_some_time"] = False


  if max_time_in_seconds is None:
    print(f"Input filename={input_filename}, alpha={alpha}, max_iter = {max_iterations}")
    best_solution, best_cost_solution, time_computing, iters = grasp(problem_cost_function, alpha, greedy_cost_function, max_iterations, data)

    visualize_solution(data, best_solution)

    print(f"Best cost of solution is {best_cost_solution}")
    print(f"Time computing: {time_computing}s")
    print(f"Iterations: {iters}")
  else:
    data["quit_computing"] = False
    threading.Timer(max_time_in_seconds, lambda x: quit_computing(data)).start()

    print(f"Input filename={input_filename}, alpha={alpha}, max_time = {max_time_in_seconds} seconds")
    best_solution, best_cost_solution, time_computing, iters = grasp_by_max_time(problem_cost_function, alpha, greedy_cost_function, max_time_in_seconds, data)

    visualize_solution(data, best_solution)

    print(f"Best cost of solution is {best_cost_solution}")
    print(f"Time computing: {time_computing}s")
    print(f"Iterations: {iters}")




