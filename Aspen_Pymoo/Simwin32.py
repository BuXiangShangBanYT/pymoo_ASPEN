import win32com.client as win32
import win32com.client
import time
import numpy as np
import math
import pymoo.Aspen_Pymoo.SQLite.Sim_moo_sql as Sim_moo_sql
import os

# 3个全局变量 3 global variable
Application = None
SimulationName1= None
PStage = None

#自定义问题的函数 Custom problem function
def MainSim(NSTAGE,FSTAGE,RR,BR):
    AspenInput2(NSTAGE,FSTAGE,RR,BR)
    AspenRun()
    Aspen_ETHA(NSTAGE)
    AspenRun()
        
    f2= AspenF2()
    f3= AspenFfrac()
    f4= AspenF4()
    g1 = AspenG1()
    g2 = AspenG2()
    g3 = AspenG3()          
    g4 = AspenG4()   
    OutInfo(NSTAGE,FSTAGE,RR,BR)
    return [f2,f3,f4,g1,g2,g3,g4]

#ASPEN打开 ASPEN OPEN
def AspenOpen(SimulationName):
    Application.InitFromArchive2(os.getcwd()+'\Simu\\'+ SimulationName + '.bkp')
    Application.Visible = 0 #1-显示界面 Show the interface 0-不显示界面 Don't show the interface
    Application.SuppressDialogs = 1
    Application.Engine.Run2(1)
    while Application.Engine.IsRunning == 1:
        time.sleep(1)

#ASPEN关闭 AspenClose
def AspenClose():
        Application.Close()
        time.sleep(2)

#ASPEN运行 AspenRun
def AspenRun():
    Application.Reinit
    Application.Engine.Run2(1)
    while Application.Engine.IsRunning == 1:
        time.sleep(1)

#ASPEN输入 INPUT OF ASPEN PLUS 
def AspenInput2(NSTAGE,FSTAGE,RR,BR):
    #总塔板 Number of stages
    Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\\NSTAGE").Value=NSTAGE
    #再沸比 Boilup ratio
    Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\BASIS_BR").Value=BR
    #进料板 FEED STAGE
    Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\FEED_STAGE\FEED").Value=FSTAGE
    #回流比 Reflux ratio
    Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\BASIS_RR").Value=RR
    #更新水力学塔板数 UPDATA COLUMN INTERNALS ENDSTAGE
    Application.Tree.FindNode("\Data\Blocks\METHA-T2\Subobjects\Column Internals\INT-1\Subobjects\Sections\\#0\Input\CA_STAGE2\INT-1\\#0").Value=3
    Application.Tree.FindNode("\Data\Blocks\METHA-T2\Subobjects\Column Internals\INT-1\Subobjects\Sections\\#0\Input\CA_STAGE2\INT-1\\#0").Value=NSTAGE-1
    #初始化侧板质量流量  SIDE STREAM MASS FLOW
    Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\PROD_FLOW\ETHANOL").Value=200
    Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\PROD_STAGE\ETHANOL").Value=2

#1.确定采出板位置和质量流量的函数
#1.FUNC OF SIDE STAGE AND SIDE STREAM MASS FLOW
def Aspen_Pstage(NSTAGE):
    io=0
    i1=0
    X1=0
    X2=np.zeros(NSTAGE)
    X3=round(Application.Tree.FindNode("\Data\Streams\LIGHT\Output\MASSFLOW\MIXED\ETHAN-01").Value,4)
    for io in range(1,NSTAGE):
        try:
            X2[io]=Application.Tree.FindNode("\Data\Blocks\METHA-T2\Output\X_MS\\"+str(io)+"\ETHAN-01").Value
        except:
            AspenRun()
            X2[io]=Application.Tree.FindNode("\Data\Blocks\METHA-T2\Output\X_MS\\"+str(io)+"\ETHAN-01").Value
        if X2[io]>X1:
            X1=X2[io]
            i1=io
    Sim_moo_sql.PSTAGE=i1
    Sim_moo_sql.PFRAC=X1
    #0.3853-X3
    Sim_moo_sql.PFLOW=round(X3/X1,3)
    return i1
   
#2.确定采出板位置和质量流量的函数
#2.FUNC OF SIDE STAGE AND SIDE STREAM MASS FLOW
def Aspen_ETHA(NSTAGE):
    i1=Aspen_Pstage(NSTAGE)
    i2=0
    if 2<i1<NSTAGE:
        Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\PROD_STAGE\ETHANOL").Value=i1
    else:
        Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\PROD_STAGE\ETHANOL").Value=NSTAGE-2
    i2=Sim_moo_sql.PFLOW
    if i2>950:
        Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\PROD_FLOW\ETHANOL").Value=1250
    else:
        Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\PROD_FLOW\ETHANOL").Value=i2+300
    

###目标函数 TARGET FUNC==========================================================================================================================================

#年能耗计算函数 FUNC OF Annual energy consumption cost
def AspenF2():
    #再沸器能耗 Condenser Heat duty
    REB = Application.Tree.FindNode("\Data\Blocks\METHA-T2\Output\REB_DUTY").Value#再沸器能耗
    #冷凝器能耗 Reboiler Heat duty
    COND = Application.Tree.FindNode("\Data\Blocks\METHA-T2\Output\COND_DUTY").Value#冷凝器能耗
    #蒸汽 Steam 7.78$/GJ,冷凝水 condensate water 0.354$/GJ;1GJ=277.778KWH，
    RCOST=round(8000*7.78/277.778,3)
    CCOST=round(8000*0.354/277.778,3)
    #年能耗 Annual energy consumption cost
    f2 = RCOST*REB-CCOST*COND
    return f2



#年设备成本计算函数 FUNC OF Annual equipment cost
def AspenF4():
    #三元非均相共沸精馏隔壁塔流程的设计与控制研究 <---THE math fomu from academic dissertation
    NSTAGE = Application.Tree.FindNode("\Data\Blocks\METHA-T2\Input\\NSTAGE").Value
    M_s=1638.2#2018年 
    M_inst=M_s/280
    d_Col=round(Application.Tree.FindNode("\Data\Blocks\METHA-T2\Subobjects\Column Internals\INT-1\Subobjects\Sections\\#0\Input\CA_DIAM\INT-1\\#0").Value,3)
    d_col066=round(math.pow(d_Col,1.066),3)
    d_col55=round(math.pow(d_Col,1.55),3)
    h_Col=(NSTAGE-2)*1.2*0.6096
    h_col802=round(math.pow(h_Col,0.802),3)
    h_tray=round((NSTAGE-2)*0.6096)
    Q=Application.Tree.FindNode("\Data\Blocks\METHA-T2\Output\REB_DUTY").Value-Application.Tree.FindNode("\Data\Blocks\METHA-T2\Output\COND_DUTY").Value
    A=Q/0.568/10
    A_inst=round(math.pow(A,0.65),3)
    #（1）塔设备费用计算: 令换热温差ΔT=10  TOEWR equipment cost,ΔT=10 
    CSC_inst=M_inst*39793.32*d_col066*h_col802
    TC_inst=M_inst*97.243*d_col55*h_tray
    #（2）换热器设备费用 Heat exchanger equipment cost
    HEC_inst=M_inst*1775.26*A_inst
    TCC = round(CSC_inst+TC_inst+HEC_inst,3)
    f4=TCC/3
    return f4

#似乎对于最优结果没什么用的函数 seemingly useless FUNC 
def AspenFfrac():
    f5 = 0.0009-Sim_moo_sql.PFRAC
    return f5

###约束函数 Constraint FUNC==========================================================================================================================================================================


def AspenG1():
    #塔顶水含量 Constraint OF TOP STAGE WATER MASS FRAC
    g1=round(Application.Tree.FindNode("\Data\Streams\LIGHT\Output\MASSFRAC\MIXED\H2O").Value,6)-0.001
    return g1
def AspenG2():    
    #塔底甲醇含量 Constraint OF BOTTOM STAGE ETHANOL MASS FRAC
    g2 = round(Application.Tree.FindNode("\Data\Streams\HEAVY\Output\MASSFRAC\MIXED\METHA-01").Value,6)-0.0001#-0.00001#塔底甲醇含量
    return g2
def AspenG3():    
    #塔顶甲醇含量 Constraint OF TOP STAGE METHANOL MASS FRAC
    g3 = round(Application.Tree.FindNode("\Data\Streams\LIGHT\Output\MASSFRAC\MIXED\ETHAN-01").Value,7)-0.0000099#塔顶乙醇含量
    return g3
def AspenG4():
    g4=24700-Application.Tree.FindNode("\Data\Streams\LIGHT\Output\MASSFLMX\MIXED").Value
    return g4 

#连接SQLITE的函数=================================================================================================================================
#FUNC OF SQLITE CONN

def OutInfo(NSTAGE,FSTAGE,RR,BR):
    X11=np.zeros(5)
    PSTAGE = Sim_moo_sql.PSTAGE
    PFLOW = Sim_moo_sql.PFLOW
    PFRAC = Sim_moo_sql.PFRAC
    LETHA = round(Application.Tree.FindNode("\Data\Streams\LIGHT\Output\MASSFRAC\MIXED\ETHAN-01").Value,6)
    LMETHA = round(Application.Tree.FindNode("\Data\Streams\LIGHT\Output\MASSFRAC\MIXED\METHA-01").Value,6)
    LH2O = round(Application.Tree.FindNode("\Data\Streams\LIGHT\Output\MASSFRAC\MIXED\H2O").Value,6)
    HMETHA= round(Application.Tree.FindNode("\Data\Streams\HEAVY\Output\MASSFRAC\MIXED\METHA-01").Value,6)
    HH20= round(Application.Tree.FindNode("\Data\Streams\HEAVY\Output\MASSFRAC\MIXED\H2O").Value,6)
    REB = Application.Tree.FindNode("\Data\Blocks\METHA-T2\Output\REB_DUTY").Value#再沸器能耗
    COND = Application.Tree.FindNode("\Data\Blocks\METHA-T2\Output\COND_DUTY").Value#冷凝器能耗
    DCOL=round(Application.Tree.FindNode("\Data\Blocks\METHA-T2\Subobjects\Column Internals\INT-1\Subobjects\Sections\\#0\Input\CA_DIAM\INT-1\\#0").Value,3)
    Sim_moo_sql.fname(NSTAGE,FSTAGE,PSTAGE,PFLOW,PFRAC,LETHA,LMETHA,LH2O,HMETHA,HH20,REB,COND,DCOL,RR,BR)


    