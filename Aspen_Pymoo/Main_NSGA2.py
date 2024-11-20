import win32com.client as win32
import os
import pymoo.Aspen_Pymoo.Simwin32
import win32com.client
import pymoo.Aspen_Pymoo.SQLite.Sim_moo_sql
from pymoo.Aspen_Pymoo.Aspen_algo.nsga2_Reload import NSGA2_Reload
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
import math
import pymoo.Aspen_Pymoo.SQLite.Sim_moo_sql
import numpy as np
from pymoo.core.problem import ElementwiseProblem



database='ASPEN_TAC'
pymoo.Aspen_Pymoo.Simwin32.SimulationName1='AA_Metha'
pymoo.Aspen_Pymoo.SQLite.Sim_moo_sql.DBname=os.getcwd()+'\SQLite\Database\\'+database+'.db'
pymoo.Aspen_Pymoo.SQLite.Sim_moo_sql.CreateDB()
pymoo.Aspen_Pymoo.Simwin32.Application = win32com.client.Dispatch('Apwn.Document.37.0')
pymoo.Aspen_Pymoo.Simwin32.AspenOpen(pymoo.Aspen_Pymoo.Simwin32.SimulationName1)

class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=4,#变量 X
                         n_obj=2,#目标 F
                         n_constr=4,#约束 G
                         xl=np.array([2.2,0.25,17,2.2]),
                         xu=np.array([4.8,0.75,46,4.8]))

    def _evaluate(self, xx, out, *args, **kwargs):
        #初始化 INITIALIZE
        NSTAGE=0
        FSTAGE=0
        RR=0
        BR=0
        #赋值 assignment statement
        NSTAGE=math.floor(xx[2])
        FSTAGE=math.floor(xx[1]*xx[2])
        RR=round(xx[0],3)
        BR=round(xx[3],3)
        XX1=np.zeros(7)
        XX1=pymoo.Aspen_Pymoo.Simwin32.MainSim(NSTAGE,FSTAGE,RR,BR)
        f2=XX1[0]
        f4=XX1[2]
        g1=XX1[3]
        g2=XX1[4]
        g3=XX1[5]
        g4=XX1[6]

        out["F"] = [f2,f4]
        out["G"] = [g1,g2,g3,g4]
        
problem = MyProblem()


algorithm = NSGA2_Reload(pop_size=100)
res = minimize(problem,
               algorithm,
               ('n_gen', 100),
               seed=1,
               verbose=True)


X = res.X
F = res.F



print("Best solution found: F=%s" % res.F)
print("Corresponding X=%s" % res.X)


plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()

#ASPEN PLUS QUIT
pymoo.Aspen_Pymoo.Simwin32.AspenClose()