from http.server import executable
import pyomo.environ as pyEnv

import re

def getCosts(filename):

    file = open(filename)
    lines = file.readlines()
    file.close()

    costs = []
    n = len(lines)
    for i in range(n):
        line_list = re.split('\t| ',lines[i][:-1]) #Spaw to ka8e line sta tabs
        line_list = [int(j) for j in line_list if j!='']
        costs.append(line_list)
    return (costs,n)

(costs, n) = getCosts('17.txt')

#Dhmiourgia model
model = pyEnv.ConcreteModel('TSP')

#deiktes i,j apo 1 ews n
model.M = pyEnv.RangeSet(n)
model.N = pyEnv.RangeSet(n)

#deiktes apo 2 ews n gia tis boh8htikes u
model.U = pyEnv.RangeSet(2,n)

#binary metablhtes apofashs x11 ews xnn
model.x = pyEnv.Var(model.N, model.M, within=pyEnv.Binary)

#Boh8htikes metablhtes u1 ews un
model.u = pyEnv.Var(model.N, within = pyEnv.NonNegativeReals, bounds = (0, n-1))

#cost matrix nxn
model.c = pyEnv.Param(model.N, model.M, initialize=lambda model, i, j: costs[i-1][j-1])

#Antikeimenikh synarthsh
def z(model):
    total_cost = sum(model.x[i,j] * model.c[i,j] for i in model.N for j in model.M)
    return total_cost

model.objective = pyEnv.Objective(rule = z, sense = pyEnv.minimize)

#periorismos1
def const1(model, M):
    #sum i gia ka8e i!=j kai j = 1,..,n
    P1 = (sum(model.x[i,M] for i in model.N if i!=M) == 1)
    return P1

model.const1 = pyEnv.Constraint(model.M,rule=const1)

#periorismos2
def const2(model, N):
    #sum j gia ka8e j!=i kai i = 1,..,n
    P2 = (sum(model.x[N,j] for j in model.M if j!=N) == 1)
    return P2

model.const2 = pyEnv.Constraint(model.M,rule=const2)

def const3(model, i, j):
    if i!=j:
        return model.u[i] - model.u[j] + model.x[i,j] * n <= n-1
    else:
        #se i == j epistrefw True
        return model.u[i] - model.u[i] == 0
        
#Pros8hkh periorismou 3 gia i,j = 2,..,n
model.const3 = pyEnv.Constraint(model.U, model.N, rule=const3)

logname = str(n) + 'log.txt'
solver = pyEnv.SolverFactory('glpk', executable = 'glpk-4.65\w64\glpsol')
result = solver.solve(model, logfile=logname)
model.solutions.store_to(result)