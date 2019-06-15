## What is it?
Project for course "Algorithmic Methods for Mathematical Models" at FIB Barcelona

## What problems are we solving?
We are solving optimization problem. Basically problem can be framed as "mixed integer programming" problem.

## Task description
Our task is to find out optimal transportation of packages using available trucks.
We aim to optimally schedule transporation of packages given that the trucks have limited capacity and packages have certain weight.

## What approach do we use?
We solve problems using 2 different approaches:
- using CPLEX studio to solve "mixed integer program"
- using heuristics (specifically GRASP with local search)

We compare results from both approaches and conclude that even though heuristics do not converge to global optimum, they are significantly faster than CPLEX studio for bigger problem instances (more packages / trucks).
