import numpy as np 

def compute_load_of_truck(solution, truck, input):
  assigned_packages = np.where(solution["pt"][:,truck] == 1)[0]
  load = 0

  for assigned_package in assigned_packages:
    load += input["packageWeight"][assigned_package]

  return load


def compute_highest_loaded_truck(input, solution):
  pt = solution['pt']

  assigned_trucks = np.unique(np.where(pt == 1)[1])

  highest_load = 0
  highest_load_index = None

  for truck in assigned_trucks:
    packages = np.where(pt[:,truck] == 1)[0]
    truck_load = 0

    for package in packages:
      truck_load += input["packageWeight"][package]

    if truck_load > highest_load:
      highest_load = truck_load
      highest_load_index = truck

  return (highest_load, highest_load_index)
