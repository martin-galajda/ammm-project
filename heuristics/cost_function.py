import numpy as np

def problem_cost_function(input, solution):
  # wTruck ∗ number of used trucks + load of the truck with the highest load
  weight_truck = input["capacityTruck"]
  trucks_used = np.where(solution["pt"] == 1)[1]

  number_of_used_trucks = len(np.unique(trucks_used))
  highest_loaded_truck = solution["highest_loaded_truck_load"]

  return (weight_truck * number_of_used_trucks) + highest_loaded_truck
