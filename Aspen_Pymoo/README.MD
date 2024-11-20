# 1. Preface
This is my first time to upload the project, if there is any infringement, please inform me to delete it.
I am not a professional programmer, not a scholar specializing in ASPEN PLUS, nor a scholar in the field of evolutionary algorithms, but I once used relevant random algorithms combined with ASPEN PLUS in my undergraduate graduation design (but it failed). A few years after graduation, one day I suddenly came to feel, so spent some time to do this job.
In the process of doing this work, I found that there are still few relevant materials in the field of ASPEN random optimization, so I share this project. If you are a senior chemical engineering student and hope to use stochastic algorithm in your graduation project, I think my sharing can help you to some extent. If you are a professional scholar, programmer or enthusiast willing to communicate with me, please feel free to contact me.
# 2. About this work
This project provides an example of NSGA2 optimizing ASPEN PLUS V11, using the open source project PYMOO 0.6.1.1. The distillation target is AA grade methanol, the optimization target is the minimum annual cost of the distillation tower, and the concentration of the waste water at the bottom of the tower needs to be met.
To test this example, simply download PYMOO, then place the project in the root directory of PYMOO and run Main_NSGA2.py. (...\site-packages\pymoo\Aspen_Pymoo), Running time 6-7 hours（on the ROG STRIX G713PV）, then you can get a Pareto front diagram and the corresponding solution.

If you are optimizing ASPEN PLUS for the first time using a multi-objective optimization algorithm and want to build your own project with reference to this project, the following may be useful:
In this project
1. The bkp file of ASPEN PLUS is stored in the Simu folder.
2. The optimization method is stored in Aspen_algo (only a piece of code is added to the original NSGA2 code to restart ASPEN PLUS every iteration of the algorithm, so as to avoid ASPEN crash due to excessive errors and algorithm failure to a certain extent).
3. Each solution is stored in the SQLITE\DATABASE folder through SQLITE.
4. Call SQLITE functions stored in SQLITE\Sim_moo_sql.py
5. Call ASPEN PLUS connect, close, enter, and read functions stored in Simwin32.py
6. Optimized methods and custom questions are stored in Main_NSGA2.py