import math
import json 

def compute_num_of_constraints_from_input(input):
  t_length = input['tLength']
  p_length = input['pLength']

  truck_x = input['xTruck']
  truck_y = input['yTruck']

  # Objective function
  constraints = 1

  # Constraint 1
  constraints += t_length
  
  # Constraint 2
  constraints += p_length

  # Constraint 3
  constraints += (math.factorial(p_length) / math.factorial(p_length - 2)) * t_length * truck_x * truck_y
  
  # Constraint 4
  constraints += p_length * truck_x * truck_y
  
  # Constraint 5
  constraints += p_length * truck_x * truck_y
  
  # Constraint 6
  constraints += t_length
  
  # Constraint 7
  constraints += (math.factorial(p_length) / math.factorial(p_length - 2)) * t_length
  
  # Constraint 8
  constraints += p_length
  
  # Constraint 9
  constraints += p_length * truck_x * truck_y

  # Constraint 10
  constraints += t_length

  return constraints

def compute_num_of_constraints(input_filename):
  with open(input_filename) as file_handle:
    input = json.loads(file_handle.read())
  return compute_num_of_constraints_from_input(input)

def compute_num_of_variables_from_input(input):
  p_length = input["pLength"]
  t_length = input["tLength"]

  truck_x = input["xTruck"]
  truck_y = input["yTruck"]

  variables = p_length * t_length

  variables += p_length * truck_x * truck_y

  variables += p_length * truck_x * truck_y

  variables += 1

  variables += t_length

  return variables

def compute_variables(input_filename):
  with open(input_filename) as file_handle:
    input = json.loads(file_handle.read())
  return compute_num_of_variables_from_input(input)
