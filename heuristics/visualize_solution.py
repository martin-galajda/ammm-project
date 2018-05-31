import numpy as np

def visualize_solution(input, solution):
  t_length = input["tLength"]
  p_length = input["pLength"]
  x_length = input["xTruck"]
  y_length = input["yTruck"]

  pxy = solution["pxy"]
  pt = solution["pt"]

  truck_pkg_position_map = -np.ones((t_length, x_length, y_length), dtype=np.int64)

  for truck in range(t_length):
    for package in range(p_length):
      if pt[package,truck] == 1:
        for x in range(x_length):
          for y in range(y_length):
            if pxy[package, x, y] == 1:
              if truck_pkg_position_map[truck, x, y] != -1:
                print(f"Already occupied by {truck_pkg_position_map[truck, x, y]}")
              truck_pkg_position_map[truck, x, y] = int(package)
  
  for truck in range(t_length):
    print(f"Truck: ${truck}")

    for y in range(y_length):
      row_truck = ""
      for x in range(x_length):
        if truck_pkg_position_map[truck, x, y] != -1:
          row_truck += f"p{truck_pkg_position_map[truck, x, y]}"
        else:
          row_truck += "=="


      print(row_truck)

    print("End")
 	 
  print(solution)
