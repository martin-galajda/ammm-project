def update_pxy(input, solution, p, new_pbl):
  package_width = input["packageX"][p]
  package_height = input["packageY"][p]

  x_start_offest, y_start_offset = new_pbl
  for another_x in range(package_width):
    current_x = int(x_start_offest + another_x)
    for another_y in range(package_height):
      current_y = int(y_start_offset - another_y)

      solution["pxy"][p,current_x,current_y] = 1

  return solution