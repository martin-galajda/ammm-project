import numpy as np 

def get_first_possible_pbl(input, solution, package, truck):
  p_length, x_truck, y_truck = solution["pxy"].shape
  package_width = input["packageX"][package]
  package_height = input["packageY"][package]
  pxy = solution["pxy"]

  new_pbl_for_package = None
  x_start_offset = 0

  packages_in_truck = np.where(solution["pt"][:,truck] == 1)[0]

  # TODO: optimize using this
  # maximum_start_x = x_truck - package_width
  # maximum_start_y = y_truck - package_height

  while new_pbl_for_package is None and x_start_offset <= (x_truck - package_width):
    y_start_offset = y_truck - 1
    while new_pbl_for_package is None and y_start_offset >= (0 + package_height):
      out_of_range_x = (x_start_offset + package_width) >= x_truck
      out_of_range_y = (y_start_offset - package_height) < 0
      point_can_be_new_pbl = not (out_of_range_x or out_of_range_y)

      if not point_can_be_new_pbl:
        y_start_offset = y_start_offset - 1
        continue

      for another_x in range(package_width):
        for another_y in range(package_height):
          current_x = x_start_offset + another_x
          current_y = y_start_offset - another_y
          
          out_of_range_x = current_x >= x_truck
          out_of_range_y = current_y < 0

          if out_of_range_x or out_of_range_y:
            point_can_be_new_pbl = False
            continue

          occupied = np.any(pxy[packages_in_truck, current_x, current_y] == 1)

          point_can_be_new_pbl = point_can_be_new_pbl and not occupied

      if point_can_be_new_pbl:
        new_pbl_for_package = (x_start_offset, y_start_offset)

      y_start_offset = y_start_offset - 1
    x_start_offset = x_start_offset + 1

  if new_pbl_for_package is None:
    return (False, (0, 0))

  return (True, new_pbl_for_package)