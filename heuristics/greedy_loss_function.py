import numpy as np 

def greedy_loss_function(input, solution, potential_element_solution):
  p, t = potential_element_solution
  # TODO: Implement

  already_assigned_truck = np.any(solution["pt"][:,t] == 1)

  number_of_possibilities_for_p = len(np.where(solution['possible_pbl'][p,:,:] == 1)[0])

  greedy_cost = int(already_assigned_truck) * -500
  greedy_cost += number_of_possibilities_for_p * -100

  x_package = input["packageX"][p]
  y_package = input["packageY"][p]
  size_of_package = x_package * y_package

  greedy_cost += size_of_package * 150

  return greedy_cost + 10
