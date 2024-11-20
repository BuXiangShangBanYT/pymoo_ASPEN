   借助Pymoo，做了一个ASPEN PLUS和Pymoo联用的案例，这是我第一次使用Github，如果有侵权，请告知我删除。所有相关代码在pymoo\\Aspen_Pymoo中。

   本人不是专业程序员，不是专门研究ASPEN PLUS的学者，也不是启发式算法领域的学者，只是曾在本科毕业设计中使用过相关随机算法与ASPEN PLUS联动（但比较失败）。 毕业几年后，突然有了灵感，于是花了一些时间完成了这项工作

   在做这项工作的过程中我发现ASPEN随机优化领域的相关资料仍然比较少，故此项目分享出来。


   With the help of Pymoo, I made a case of the combination of ASPEN PLUS and Pymoo. This is my first time using Github. In case of infringement, please let me know to delete it. All relevant code is in pymoo\\Aspen_Pymoo.

   I am not a professional programmer, not a scholar specializing in ASPEN PLUS, nor a scholar in the field of born algorithms, but I once used related stochastic algorithms to linkage with ASPEN PLUS in my undergraduate graduation design (but failed). A few years after graduation, So-and-so suddenly had a feeling one day, so it took some time to finish the work

   In the process of doing this work, I found that the relevant information in the field of ASPEN random optimization is still relatively small, so this project is shared.

.. | 蟒蛇|图片:: https://img.shields.io/badge/python-3.10-blue.svg
   ：替代：Python 3.10

.. |许可证|图片:: https://img.shields.io/badge/license-apache-orange.svg
   :alt: 许可阿帕奇
   ：目标：https://www.apache.org/licenses/LICENSE-2.0


..|标志|图片:: https://github.com/anyoptimization/pymoo-data/blob/main/logo.png?raw=true
  ：目标：https://pymoo.org
  ： 替代： pymoo


.. |动画|图片:: https://github.com/anyoptimization/pymoo-data/blob/main/animation.gif?raw=true
  ：目标：https://pymoo.org
  ： 替代： pymoo


.._Github：https://github.com/anyoptimization/pymoo
.._文档：https://www.pymoo.org/
.._论文：https://ieeexplore.ieee.org/document/9078759




| 蟒蛇| |许可证|


| 标志|



文档_ / 论文_ / 安装_ / 使用_ / 引用_ / 联系方式_



pymoo：Python中的多目标优化
=================================================== =================

我们的开源框架 pymoo 提供最先进的单目标和多目标算法以及更多功能
与多目标优化相关，例如可视化和决策制定。


.._安装：

安装
****************************************************** **********************************

First, make sure you have a Python 3 environment installed. We recommend miniconda3 or anaconda3.

The official release is always available at PyPi:

.. code:: bash

    pip install -U pymoo


For the current developer version:

.. code:: bash

    git clone https://github.com/anyoptimization/pymoo
    cd pymoo
    pip install .


Since for speedup, some of the modules are also available compiled, you can double-check
if the compilation worked. When executing the command, be sure not already being in the local pymoo
directory because otherwise not the in site-packages installed version will be used.

.. code:: bash

    python -c "from pymoo.util.function_loader import is_compiled;print('Compiled Extensions: ', is_compiled())"


.. _Usage:

Usage
********************************************************************************

We refer here to our documentation for all the details.
However, for instance, executing NSGA2:

.. code:: python


    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.problems import get_problem
    from pymoo.optimize import minimize
    from pymoo.visualization.scatter import Scatter

    problem = get_problem("zdt1")

    algorithm = NSGA2(pop_size=100)

    res = minimize(problem,
                   algorithm,
                   ('n_gen', 200),
                   seed=1,
                   verbose=True)

    plot = Scatter()
    plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
    plot.add(res.F, color="red")
    plot.show()



A representative run of NSGA2 looks as follows:

|animation|



.. _Citation:

Citation
********************************************************************************

If you have used our framework for research purposes, you can cite our publication by:

| `J. Blank and K. Deb, pymoo: Multi-Objective Optimization in Python, in IEEE Access, vol. 8, pp. 89497-89509, 2020, doi: 10.1109/ACCESS.2020.2990567 <https://ieeexplore.ieee.org/document/9078759>`_
|
| BibTex:

::

    @ARTICLE{pymoo,
        author={J. {Blank} and K. {Deb}},
        journal={IEEE Access},
        title={pymoo: Multi-Objective Optimization in Python},
        year={2020},
        volume={8},
        number={},
        pages={89497-89509},
    }

.. _Contact:

Contact
********************************************************************************

Feel free to contact me if you have any questions:

| `Julian Blank <http://julianblank.com>`_  (blankjul [at] msu.edu)
| Michigan State University
| Computational Optimization and Innovation Laboratory (COIN)
| East Lansing, MI 48824, USA



