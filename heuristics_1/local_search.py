import numpy as np
from collections import deque

import load_computer
import random
import time
from itertools import combinations
from can_be_assigned_to_truck import can_be_assigned_to_truck
from update_pxy import update_pxy

def create_copy_of_solution(solution):
  """
    Creates a copy of solution and returns it.

    Args:
      solution (dict)

    Returns:
      new copied solution (dict)
  """
  solution_copy = {
    'pt': solution["pt"].copy(),
    'pbl': solution["pbl"].copy(),
    'pxy': solution["pxy"].copy(),
    'usedTruck': solution["usedTruck"].copy(),
    'highest_loaded_truck_load': solution["highest_loaded_truck_load"],
    'highest_loaded_truck_index': solution["highest_loaded_truck_index"],
  }

  return solution_copy


def construct_neighbourhood(input, feasible_solution, distance = 1):
  """
    Construct a neighbourhood for feasible solution -> generates theoretically possible different solutions with given distance.
    Distance in this problem represent number of packages which will be assigned to different trucks.

    Args:
      input (dict) -- input given for the problem
      feasible_solution (disct) -- feasible solution achieved
      distance[=1] (int) -- distance of the neighbourhood (how many packages to reassign from feasible solution)
    Returns:
      list of alternative assignments (solution) that may be feasible but do not need
  """
  pt_assigned = np.where(feasible_solution["pt"] == 1)
  tLength = input['tLength']

  package_truck_assignments_count = len(pt_assigned[0])

  set_of_all_combinations_to_remove_pt_assignments = combinations(np.arange(0, package_truck_assignments_count), distance)
  all_possible_alternatives = []

  set_of_all_combinations_to_remove_pt_assignments = list(set_of_all_combinations_to_remove_pt_assignments)

  random.shuffle(set_of_all_combinations_to_remove_pt_assignments)

  for combinations_to_reassign in set_of_all_combinations_to_remove_pt_assignments:
    new_alternatives = []
    for combination_element in combinations_to_reassign:
      remove_assignment = (pt_assigned[0][combination_element], pt_assigned[1][combination_element])
      package_unassigned = remove_assignment[0]
      truck_unassigned = remove_assignment[1]

      new_alternative = {
        'remove_p': package_unassigned,
        'remove_t': truck_unassigned,
        'new_pt_possible_assignments': [(package_unassigned, truck) for truck in range(0, tLength) if truck != truck_unassigned]
      }
      new_alternatives += [new_alternative]

    all_possible_alternatives += [new_alternatives]

  return all_possible_alternatives

def remove_assignment_from_solution(input, solution, p, t):
  """
    Creates copy of solution in which given assignment of package to the truck is removed.
    Args:
      input (dict)
      solution (dict)
      p (int) -- package index
      t (int) -- truck index

    Returns:
      Alternative copied solution without package p assigned to truck t.
  """
  alternative_solution = create_copy_of_solution(solution)
  alternative_solution['pxy'][p,:,:] = 0
  alternative_solution['pbl'][p,:,:] = 0
  alternative_solution['pt'][p,t] = 0
  alternative_solution['usedTruck'][t] = len(np.where(alternative_solution['pt'][:,t] == 1)[0]) > 0

  if alternative_solution['highest_loaded_truck_index'] == t:
    highest_load_truck_load, highest_loaded_truck_idx = load_computer.compute_highest_loaded_truck(input, alternative_solution)
    alternative_solution['highest_loaded_truck_load'] = highest_load_truck_load
    alternative_solution['highest_loaded_truck_index'] = highest_loaded_truck_idx

  return alternative_solution

def construct_alternative_solution_set(cost_function, input, feasible_solution, use_only_best=True):
  cost_feasible_solution = cost_function(input, feasible_solution)
  best_cost_seen = cost_feasible_solution

  alternative_solution_set = deque()
  best_in_neighbourhood = feasible_solution

  all_possible_alternative_combinations = construct_neighbourhood(input, feasible_solution)

  for possible_alternatives in all_possible_alternative_combinations:
    # start from the feasible solution and recursively construct alternative by using combinations of different reassignment
    alternative_solutions = [create_copy_of_solution(feasible_solution)]

    found_feasible_solutions = []
    for possible_alternative in possible_alternatives:
      p = possible_alternative['remove_p']
      t = possible_alternative['remove_t']
      new_pt_assignments = possible_alternative['new_pt_possible_assignments']
      current_alternative_solutions = []

      for alternative_solution in alternative_solutions:
        new_alternative_solution = remove_assignment_from_solution(input, alternative_solution, p, t)

        for pt_assignment in new_pt_assignments:
          new_p = pt_assignment[0]
          new_t = pt_assignment[1]

          assignable, new_pbl = can_be_assigned_to_truck(input, new_alternative_solution, new_p, new_t)
          if not assignable:
            continue

          new_feasible_alternative_solution = create_copy_of_solution(new_alternative_solution)
          new_feasible_alternative_solution['pt'][new_p,new_t] = 1
          new_feasible_alternative_solution['pbl'][new_p,new_pbl[0], new_pbl[1]] = 1
          new_feasible_alternative_solution['usedTruck'][new_t] = 1

          # update pxy
          new_feasible_alternative_solution = update_pxy(input, new_feasible_alternative_solution, new_p, new_pbl)

          # update
          highest_load_truck_load, highest_loaded_truck_idx = load_computer.compute_highest_loaded_truck(input, new_feasible_alternative_solution)
          new_feasible_alternative_solution['highest_loaded_truck_load'] = highest_load_truck_load
          new_feasible_alternative_solution['highest_loaded_truck_index'] = highest_loaded_truck_idx

          found_feasible_solutions += [new_feasible_alternative_solution]
          current_alternative_solutions += [new_feasible_alternative_solution]
      alternative_solutions = current_alternative_solutions

    for alternative_solution in found_feasible_solutions:
      # check cost of new solution, add it to H if has better cost
      cost = cost_function(input, alternative_solution)

      if not use_only_best and cost < cost_feasible_solution:
        # add it to the H
        alternative_solution_set.append(alternative_solution)

      if cost < best_cost_seen:
        best_cost_seen = cost
        best_in_neighbourhood = alternative_solution

  if use_only_best and best_cost_seen < cost_feasible_solution:
    alternative_solution_set = deque()
    alternative_solution_set.append(best_in_neighbourhood)

  return (alternative_solution_set, best_cost_seen, best_in_neighbourhood)

def local_search(cost_function, input, feasible_solution):
  solution_set, best_cost_seen, best_solution = construct_alternative_solution_set(cost_function, input, feasible_solution)
  best_cost_seen = cost_function(input, feasible_solution)
  best_solution = feasible_solution

  while len(solution_set) > 0:
    another_feasible_solution = solution_set.pop()
    another_solution_set, another_best_cost_seen, another_best_solution = construct_alternative_solution_set(cost_function, input, another_feasible_solution)
    solution_set.extend(another_solution_set)

    if another_best_cost_seen < best_cost_seen:
      best_cost_seen = another_best_cost_seen
      best_solution = another_best_solution

  return (best_cost_seen, best_solution)
