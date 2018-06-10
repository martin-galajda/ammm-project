import numpy as np
import math
import load_computer
import sys
import time

from update_pxy import update_pxy
from can_be_assigned_to_truck import can_be_assigned_to_truck

def update_candidate_set(input, solution, candidate_set, new_element_solution):
  possible_pt = candidate_set

  p, t = new_element_solution
  # Make newly assigned package unavailable for every truck
  possible_pt[p,:] = 0

  # Get package which has to be updated
  # truck_updated = np.where(solution["pt"][p, ] == 1)[0][0]
  packages_to_be_checked = np.where(possible_pt[:,t] == 1)[0]

  # for every package that could be assigned to the truck before
  # check if it can be still assigned to the truck and recompute precomputed pbl point
  for package in packages_to_be_checked:
    if package == p:
      continue
    possible_pt[package,t], solution["possible_pbl"][package, t] = can_be_assigned_to_truck(input, solution, package, t)

    if possible_pt[package,t] == 0:
      print(f"Removing possibility to select p{package} into t{t}, after p{p},t{t} assignment")
      print(f"Size of p{p} is {input['packageX'][p]},{input['packageY'][p]}")
      print(f"Capacity of p{p} is {input['packageWeight'][p]}")

  return possible_pt

def add_new_solution(input, solution, new_element_solution):
  p, t = new_element_solution

  # Find first bottom-left coordinate that is free
  new_pbl_for_package = solution["possible_pbl"][p,t]

  if new_pbl_for_package is (-1, -1):
    print(f"Something went wrong!!!. Adding new solution failed - new pbl was not found")
    sys.exit()

  solution = update_pxy(input, solution, p, new_pbl_for_package)

  solution["pbl"][p, int(new_pbl_for_package[0]), int(new_pbl_for_package[1])] = 1.0
  solution["usedTruck"][t] = 1
  solution["pt"][p,t] = 1

  load_of_truck = load_computer.compute_load_of_truck(solution, t, input)

  if load_of_truck > solution["highest_loaded_truck_load"]:
    solution["highest_loaded_truck_load"] = load_of_truck
    solution["highest_loaded_truck_index"] = t

  return solution

def initialize_solution(input):
  xTruck = input["xTruck"]
  yTruck = input["yTruck"]
  pLength = input["pLength"]
  tLength = input["tLength"]

  usedTruck = np.zeros(tLength)
  pxy = np.zeros((pLength, xTruck, yTruck))
  pbl = np.zeros((pLength, xTruck, yTruck))
  pt = np.zeros((pLength, tLength), dtype=np.int64)

  empty_solution = {
    'pxy': pxy,
    'pbl': pbl,
    'pt': pt,
    'usedTruck': usedTruck,
    'possible_pbl': np.zeros((pLength, tLength), dtype=(np.int64, 2)),
    'highest_loaded_truck_load': 0,
    'highest_loaded_truck_index': None
  }

  empty_solution['possible_pbl'][:,:,1] = yTruck - 1

  return empty_solution

def initialize_candidate_set(input, solution):
  t_length = input["tLength"]
  p_length = input["pLength"]

  # Assume that initially we have a dataset that contains feasible solution?
  pt = np.ones((p_length, t_length), dtype=np.int64)

  return pt


def get_element_loss_range(greedy_loss_function, input, solution, candidate_set, params_glf = None):
  precomputed_greedy_cost_package_truck = np.repeat(-math.inf, (input["pLength"] * input["tLength"])).reshape(input["pLength"], input["tLength"])

  possible_assignments = np.where(candidate_set == 1)

  min = None
  max = None

  for possible_assignment_idx in range(len(possible_assignments[0])):
    p = possible_assignments[0][possible_assignment_idx]
    t = possible_assignments[1][possible_assignment_idx]

    precomputed_greedy_cost_package_truck[p,t] = greedy_loss_function(input, solution, (p, t), candidate_set, params_glf)

    if min is None or precomputed_greedy_cost_package_truck[p,t] < min:
      min = precomputed_greedy_cost_package_truck[p,t]

    if max is None or precomputed_greedy_cost_package_truck[p,t] > max:
      max = precomputed_greedy_cost_package_truck[p,t]


  return (min, max, precomputed_greedy_cost_package_truck)

def random_select(candidate_solutions):
  random_element_idx = np.random.choice(len(candidate_solutions[0]), 1)[0]

  return (candidate_solutions[0][random_element_idx], candidate_solutions[1][random_element_idx])

def get_candidate_solutions(min, max, precomputed_cost, alpha):
  margin = (max - min) * alpha

  possible_solutions = np.where( (precomputed_cost != -math.inf) & (precomputed_cost <= min + margin) )

  return possible_solutions

def try_to_construct_solution(greedy_loss_function, alpha, input, params_glf = None):
  solution = initialize_solution(input)
  candidate_set = initialize_candidate_set(input, solution)

  while len(np.where(candidate_set == 1)[0]) > 0:
    min, max, precomputed_cost = get_element_loss_range(greedy_loss_function, input, solution, candidate_set, params_glf)

    candidate_solutions = get_candidate_solutions(min, max, precomputed_cost, alpha)
    new_element_solution = random_select(candidate_solutions)

    add_new_solution(input, solution, new_element_solution)

    candidate_set = update_candidate_set(input, solution, candidate_set, new_element_solution)

  return solution

def check_solution_correctness(input, solution):
  pt_obtained = solution['pt']
  package_weight = input['packageWeight']
  pLength = input['pLength']
  tLength = input['tLength']
  for truck in range(tLength):
    capacity_used = 0
    for package in range(pLength):
      if pt_obtained[package, truck]:
        capacity_used += package_weight[package]


    if capacity_used > 500:
      print(f"Normal construct screwed up")
      sys.exit()

  number_of_trucks_assigned_to_package = solution['pt'].sum(axis = 1)

  if len(np.where(number_of_trucks_assigned_to_package > 1)[0]) > 0:
    print(solution)
    print("Constructive fucked up for row > 1")
    sys.exit()


def construct(greedy_loss_function, alpha, input, params_gcf = None):
  feasible_solution_obtained = False

  infeasible_solutions_achieved = -1
  
  while not feasible_solution_obtained:
    if input["stop_after_some_time"] == True:
      if time.time() - input["time_start"] > input["max_time"]:
        return None
    solution = try_to_construct_solution(greedy_loss_function, alpha, input, params_gcf)

    number_of_trucks_assigned_to_package = solution['pt'].sum(axis = 1)

    # TODO: remove after debugging
    if len(np.where(number_of_trucks_assigned_to_package > 1)[0]) > 0:
      print(solution)
      print("Constructive fucked up for row > 1")
      sys.exit()
    # TODO: remove after debugging

    packages_not_assigned = len(np.where(number_of_trucks_assigned_to_package == 0)[0])
    feasible_solution_obtained = packages_not_assigned == 0
    infeasible_solutions_achieved += 1
    

  # TODO: remove debugging
  check_solution_correctness(input, solution)
  # TODO: remove debugging

  print(f"Infeasible solutions achieved in construct: {infeasible_solutions_achieved}")

  return solution
