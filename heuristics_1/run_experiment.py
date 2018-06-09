import math
import json
import pprint
import numpy as np
import json
import time
import os


from visualize_solution import visualize_solution
from grasp import grasp
from cost_function import problem_cost_function
from greedy_loss_function import greedy_loss_function
from grasp_time import grasp_by_max_time
import compute_instance_size

def write_results(input, best_cost_solution, iterations, time_computing, input_filename, alpha):
  dir_path = os.path.dirname(os.path.realpath(__file__))
  input_filename_substr_start = input_filename.rfind("/")
  input_filename_substr_end = input_filename.rfind(".json")
  input_filename = input_filename[input_filename_substr_start+1:input_filename_substr_end]

  filename = f"{dir_path}/results/{input_filename}.csv"

  instance_size = compute_instance_size.compute_num_of_constraints_from_input(input) + compute_instance_size.compute_num_of_variables_from_input(input)
  result = f"{best_cost_solution},{iterations},{time_computing},{instance_size},{alpha}{os.linesep}"

  with open(filename, "a") as myfile:
    myfile.write(result)
  

def run_experiment(input_filename, alpha = 0.8, max_iterations = 1000, max_time_in_seconds = None):
  with open(input_filename) as file_handle:
    data = json.loads(file_handle.read())

  if max_time_in_seconds is None:
    print(f"Input filename={input_filename}, alpha={alpha}, max_iter = {max_iterations}")
    best_solution, best_cost_solution, time_computing, iters = grasp(problem_cost_function, alpha, greedy_loss_function, max_iterations, data)

    visualize_solution(data, best_solution)

    print(f"Best cost of solution is {best_cost_solution}")
    print(f"Time computing: {time_computing}s")
    print(f"Iterations: {iters}")
    write_results(data, best_cost_solution, iters, time_computing, input_filename, alpha)
  else:
    print(f"Input filename={input_filename}, alpha={alpha}, max_time = {max_time_in_seconds} seconds")
    best_solution, best_cost_solution, time_computing, iters = grasp_by_max_time(problem_cost_function, alpha, greedy_loss_function, max_time_in_seconds, data)

    visualize_solution(data, best_solution)

    print(f"Best cost of solution is {best_cost_solution}")
    print(f"Time computing: {time_computing}s")
    print(f"Iterations: {iters}")
    write_results(data, best_cost_solution, iters, time_computing, input_filename, alpha)




