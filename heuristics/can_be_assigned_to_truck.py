import numpy as np
from get_first_possible_pbl import get_first_possible_pbl

def can_be_assigned_to_truck(input, solution, package, truck):
  pt = solution['pt']

  # Get packages assigned to truck
  packages_assigned_to_truck = np.where(pt[:,truck] == 1)[0]

  # Compute capacity left
  package_weight = input['packageWeight']
  truck_capacity_left = input['capacityTruck']

  for package_assigned in packages_assigned_to_truck:
    truck_capacity_left -= package_weight[package_assigned]

  np_input_incomp = np.array(input["incomp"])
  is_incomp = np.any(np_input_incomp[packages_assigned_to_truck, package] == 1) or np.any(np_input_incomp[package, packages_assigned_to_truck] == 1)

  if is_incomp:
    return (False, (-1, -1))

  if truck_capacity_left < package_weight[package]:
    return (False, (-1, -1))

  # Check coordinates, if there is possibility for package to fit
  # Find first bottom-left coordinate that is free and return it
  possible_pbl_exists, new_pbl_for_package = get_first_possible_pbl(input, solution, package, truck)
  if not possible_pbl_exists:
    return (False, (-1, -1))

  return (True, new_pbl_for_package)