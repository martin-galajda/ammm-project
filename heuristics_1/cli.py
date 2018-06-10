import sys
from os import listdir, linesep
from os.path import isfile, join
from run_experiment import run_experiment
from grasp_time import grasp_by_max_time
from grasp import grasp

from compute_instance_size import compute_num_of_constraints
from tune_parameters import tune_params

class Shell():
  def cmdloop(self, root = './experiment_instances_v2'):
    onlyfiles = [f for f in listdir(root) if isfile(join(root, f)) and f.find('.json') != -1 ]
    str1 = ''.join(f"{str(filename)} OPTION ({str(idx)}) " + '\n' for idx, filename in enumerate(onlyfiles))
    filename_idx = input(f"Which experiment do u want to run? Enter number: {linesep}{str1}{linesep}>>> ")
    filename = f"./experiment_instances_v2/{onlyfiles[int(filename_idx)]}"

    question = f"What do you want to do? {linesep} (1): Run GRASP and write results. {linesep} (2): Compute num of constraints. {linesep}"
    question += f"Enter just number 1/2/3:{linesep}>>> "

    option = input(question)

    if option == "2":
      print(f"{compute_num_of_constraints(filename)} constraints")
      sys.exit()
    elif option == "1":
      self.run_experiment(filename)
    else:
      print(f"Invalid option: {option}")
  def run_grasp(self, filename):
    alpha = input(f"What alpha to use? Enter number (default 0.8):{linesep}>>> ")

    try:
      alpha = float(alpha)
    except ValueError:
      alpha = 0.8

    max_time_in_seconds = 0
    minutes = input(f"Time to compute? (in minutes):{linesep}>>> ")
    if len(minutes) > 0:
      minutes = float(minutes)
      max_time_in_seconds = minutes * 60

    run_experiment(input_filename = filename, alpha = alpha, max_time_in_seconds = max_time_in_seconds)

  def run_experiment(self, filename):
    alpha = input(f"What alpha to use? Enter number (default 0.8):{linesep}>>> ")

    try:
      alpha = float(alpha)
    except ValueError:
      alpha = 0.8

    iterations = input(f"Time to compute? (iterations):{linesep}>>> ")
    if len(iterations) > 0:
      iterations = int(iterations)

    times = input(f"How many times to run experiment?:{linesep}>>> ")
    if len(times) > 0:
      times = int(times)

    experiments_run = 0
    while experiments_run < times:
      experiments_run += 1
      run_experiment(input_filename = filename, alpha = alpha, max_iterations = iterations)



if __name__ == '__main__':
  Shell().cmdloop()
