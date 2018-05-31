import numpy as np
from collections import deque

import load_computer
from can_be_assigned_to_truck import can_be_assigned_to_truck
from update_pxy import update_pxy

def create_copy_of_solution(solution):
  solution_copy = {
    'pt': solution["pt"].copy(),
    'pbl': solution["pbl"].copy(),
    'pxy': solution["pxy"].copy(),
    'usedTruck': solution["usedTruck"].copy(),
    'highest_loaded_truck_load': solution["highest_loaded_truck_load"],
    'highest_loaded_truck_index': solution["highest_loaded_truck_index"],
  }

  return solution_copy


def construct_alternative_solution_set(cost_function, input, feasible_solution):
  pt = np.where(feasible_solution["pt"] == 1)
  cost_feasible_solution = cost_function(input, feasible_solution)
  best_cost_seen = cost_feasible_solution

  alternative_solution_set = deque()
  best_in_neighbourhood = feasible_solution

  for element_solution_index in range(len(pt[0])):
    alternative_solution = create_copy_of_solution(feasible_solution)

    p = pt[0][element_solution_index]
    t = pt[1][element_solution_index]

    alternative_solution['pxy'][p,:,:] = 0
    alternative_solution['pbl'][p,:,:] = 0
    alternative_solution['pt'][p,t] = 0
    alternative_solution['usedTruck'][t] = len(np.where(alternative_solution['pt'][:,t] == 1)[0]) > 0

    if alternative_solution['highest_loaded_truck_index'] == t:
      highest_load_truck_load, highest_loaded_truck_idx = load_computer.compute_highest_loaded_truck(input, alternative_solution)
      alternative_solution['highest_loaded_truck_load'] = highest_load_truck_load
      alternative_solution['highest_loaded_truck_index'] = highest_loaded_truck_idx
      

    for truck in range(input["tLength"]):
      if truck == t:
        continue
      
      assignable, new_pbl = can_be_assigned_to_truck(input, alternative_solution, p, truck)
      if not assignable:
        continue
        # not feasible solution, continue

      alternative_solution_copy = create_copy_of_solution(alternative_solution)

      alternative_solution_copy['pt'][p,truck] = 1
      alternative_solution_copy['pbl'][p,new_pbl[0], new_pbl[1]] = 1
      alternative_solution_copy['usedTruck'][truck] = 1

      # update pxy
      alternative_solution_copy = update_pxy(input, alternative_solution_copy, p, new_pbl)

      # update highest_loaded truck if necessary
      load_of_newly_used_truck = load_computer.compute_load_of_truck(alternative_solution_copy, truck, input)
      if load_of_newly_used_truck > alternative_solution['highest_loaded_truck_load']:
        alternative_solution_copy['highest_loaded_truck_load'] = load_of_newly_used_truck
        alternative_solution_copy['highest_loaded_truck_index'] = truck

      # check cost of new solution, add it to H if has better cost
      cost = cost_function(input, alternative_solution_copy)

      if cost < cost_feasible_solution:
        # add it to the H
        print(f"Changing [p,t] = ({p}, {t}) to [p, t] = ({p}, {truck})")
        print(f"Improved feasible sol cost = ({cost_feasible_solution}) to  = ({cost})")

        alternative_solution_set.append(alternative_solution_copy)

      if cost < best_cost_seen:
        print(f"Changing best cost seen = ({best_cost_seen}) to  = ({cost})")

        best_cost_seen = cost
        # best_solution = alternative_solution
        # alternative_solution_set.append(alternative_solution_copy)
        best_in_neighbourhood = alternative_solution_copy
        # alternative_solution_set.append(alternative_solution)

  return (alternative_solution_set, best_cost_seen, best_in_neighbourhood)

def local_search(cost_function, input, feasible_solution):
  solution_set, best_cost_seen, best_solution = construct_alternative_solution_set(cost_function, input, feasible_solution)
  
  while len(solution_set) > 0:
    another_feasible_solution = solution_set.pop()
    print(len(solution_set))

    another_solution_set, another_best_cost_seen, another_best_solution = construct_alternative_solution_set(cost_function, input, another_feasible_solution)

    # solution_set = another_solution_set
    solution_set.extend(another_solution_set)

    # print(len(solution_set))
    # print(f"Adding {len(another_solution_set)} solutions")

    if another_best_cost_seen < best_cost_seen:
      print(f"Changing best cost seen from {best_cost_seen} to {another_best_cost_seen}")
      best_cost_seen = another_best_cost_seen
      best_solution = another_best_solution

  return (best_cost_seen, best_solution)
