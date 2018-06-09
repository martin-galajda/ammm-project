import numpy as np 

default_greedy_loss_function_params = {
  'cost_already_assigned_truck': -400,
  'cost_for_possible_truck_assignment': 100,
  'cost_for_size_of_package': -15,
  'cost_for_package_weight': -3,
  'cost_for_capacity_left': 20,
  'capacity_v1': False
}

def greedy_loss_function(input, solution, potential_element_solution, parameters = default_greedy_loss_function_params):

  if parameters is None:
    parameters = default_greedy_loss_function_params
    
  p, t = potential_element_solution
  already_assigned_truck = np.any(solution["pt"][:,t] == 1)

  packages_assigned_to_truck = np.where(solution["pt"][:,t] == 1)[0]
  truck_capacity = input["capacityTruck"]
  package_weights = input["packageWeight"]
  x_package = input["packageX"][p]
  y_package = input["packageY"][p]

  capacity_left_truck = truck_capacity
  for package_assigned_to_truck in packages_assigned_to_truck:
    capacity_left_truck -= package_weights[package_assigned_to_truck]

  number_of_possibilities_for_p = len(np.where(solution['possible_pbl'][p,:,:] == 1)[0])

  greedy_cost = int(already_assigned_truck) * parameters["cost_already_assigned_truck"]
  greedy_cost += number_of_possibilities_for_p * parameters["cost_for_possible_truck_assignment"]

  size_of_package = x_package * y_package
  package_weight = package_weights[p]

  greedy_cost += size_of_package * parameters["cost_for_size_of_package"]

  if parameters["capacity_v1"]:
    greedy_cost += -((truck_capacity / capacity_left_truck) * package_weight)

  else:
    # 200 * 2 vs 10 * 2
    # 500 / 1 (500) * 200
    # by using negative value we prefer to assign packages with bigger weight
    # by using positive value we prefer to assign packages with lower weight
    # also we prefer to
    greedy_cost += package_weight * parameters["cost_for_package_weight"]

    # negative value -> we prefer
    # positive value -> we prefer
    greedy_cost += capacity_left_truck * parameters["cost_for_capacity_left"]
    # greedy_cost += ((truck_capacity / capacity_left_truck) * package_weight) * parameters["cost_for_package_weight_"]

  return greedy_cost
