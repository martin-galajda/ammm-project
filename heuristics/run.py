import math
import json
import pprint
import numpy as np
import json


from visualize_solution import visualize_solution
from grasp import grasp
from cost_function import problem_cost_function
from greedy_loss_function import greedy_loss_function

filename = '../generated-data-1527017708311.json'
with open(filename) as file_handle:
  data = json.loads(file_handle.read())

alpha = 0.8
max_iterations = 100

best_solution, best_cost_solution = grasp(problem_cost_function, alpha, greedy_loss_function, max_iterations, data)

print(f"Best cost of solution is {best_cost_solution}")

# print(best_solution)
visualize_solution(data, best_solution)

# with open('latest_solution.json', 'w') as fp:
#   json.dump(best_solution, fp, sort_keys=True, indent=4)
