import json

from grasp import grasp
from cost_function import problem_cost_function
from greedy_loss_function import greedy_loss_function
from grasp_time import grasp_by_max_time
import time, threading


params_1 = {
  'cost_already_assigned_truck': -200,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': 0,
  'cost_for_package_weight': -10,
  'cost_for_capacity_left': -0
}

params_2 = {
  'cost_already_assigned_truck': -400,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': 0,
  'cost_for_package_weight': -10,
  'cost_for_capacity_left': -0
}

params_3 = {
  'cost_already_assigned_truck': -600,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': 0,
  'cost_for_package_weight': -10,
  'cost_for_capacity_left': -0
}

params = [
  params_1, # 8, 3, 4
  params_2, # 9, 5, 7
  params_3, # 6, 5, 5
]

params_v2_1 = {
  'cost_already_assigned_truck': -300,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -10,
  'cost_for_package_weight': 0,
  'cost_for_capacity_left': 20,
  'capacity_v1': True
}

params_v2_2 = {
  'cost_already_assigned_truck': -400,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -10,
  'cost_for_package_weight': -1,
  'cost_for_capacity_left': 20,
  'capacity_v1': True
}

params_v2_4 = {
  'cost_already_assigned_truck': -500,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -10,
  'cost_for_package_weight': -3,
  'cost_for_capacity_left': 20,
  'capacity_v1': True
}
params_v2_5 = {
  'cost_already_assigned_truck': -300,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -10,
  'cost_for_package_weight': 0,
  'cost_for_capacity_left': 20,
  'capacity_v1': True
}
params_v2_6 = {
  'cost_already_assigned_truck': -400,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -10,
  'cost_for_package_weight': -1,
  'cost_for_capacity_left': 20,
  'capacity_v1': False
}
params_v2_7 = {
  'cost_already_assigned_truck': -400,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -10,
  'cost_for_package_weight': -1,
  'cost_for_capacity_left': 20,
  'capacity_v1': True
}
params_v2_8 = {
  'cost_already_assigned_truck': -400,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -10,
  'cost_for_package_weight': -3,
  'cost_for_capacity_left': 20,
  'capacity_v1': False
}
params_v2_9 = {
  'cost_already_assigned_truck': -400,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -10,
  'cost_for_package_weight': -4,
  'cost_for_capacity_left': 20,
  'capacity_v1': False
}
params_v2_10 = {
  'cost_already_assigned_truck': -400,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -15,
  'cost_for_package_weight': -3,
  'cost_for_capacity_left': 20,
  'capacity_v1': False
}

params_v2 = [
  params_v2_1, # 8
  params_v2_2, # 15
  params_v2_4, # 10
  params_v2_5, # 8
  params_v2_6, # 15
  params_v2_7, # 10
  params_v2_8, # 8
  params_v2_9, # 15
  params_v2_10, # 10
]


def quit_computing(data):
  data["quit_computing"] = True

def tune_params(input_filename, alpha = 0.8, max_time_in_seconds = 60):
  with open(input_filename) as file_handle:
    data = json.loads(file_handle.read())

  results = []

  for param in params_v2:
  
    print(f"Input filename={input_filename}, alpha={alpha}, max_time = {max_time_in_seconds} seconds")
    data["stop_after_some_time"] = True
    data["time_start"] = time.time()
    data["max_time"] = max_time_in_seconds

    best_solution, best_cost_solution, time_computing, iterations = grasp_by_max_time(problem_cost_function, alpha, greedy_loss_function, max_time_in_seconds, data, params_glf = param)

    print(f"Best cost of solution is {best_cost_solution}")
    print(f"Time computing: {time_computing}s")

    results += [(time_computing, iterations, best_cost_solution)]

  for idx, result in enumerate(results):
    print(f"Idx = {idx + 1}, Result = {result} ")
