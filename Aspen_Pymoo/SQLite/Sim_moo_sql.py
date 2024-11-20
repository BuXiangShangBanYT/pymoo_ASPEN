import sqlite3
from datetime import datetime
import os

# 连接到SQLite数据库

DBname=os.getcwd()+'\SQLite\Database\pymoo.db'
#XX=DBname+"1110"
PSTAGE = 0
PFRAC = 0
PFLOW = 50

def CreateDB():
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pymoo (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        nstage INTEGER NOT NULL,
        fstage INTEGER NOT NULL,
        pstage INTEGER NOT NULL,
        PFLOW INTEGER NOT NULL,
        PFRAC INTEGER NOT NULL,
        LETHA INTEGER NOT NULL,
        LMETHA INTEGER NOT NULL,
        LH2O INTEGER NOT NULL,
        HMETHA INTEGER NOT NULL,
        HH20 INTEGER NOT NULL,
        REB INTEGER NOT NULL,
        COND INTEGER NOT NULL,
        DCOL INTEGER NOT NULL,       
        RR INTEGER NOT NULL,
        BR INTEGER NOT NULL             
    )
''')#16个

#9个变量
def fname(X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,X11,X12,X13,X14,X15):
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor() 
    cursor.execute('''
    INSERT INTO pymoo (name, nstage,fstage,pstage,PFLOW,PFRAC,LETHA,LMETHA,LH2O,HMETHA,HH20,REB,COND,DCOL,RR,BR)
    VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
''',('ASPEN PLUS',X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,X11,X12,X13,X14,X15))
    conn.commit()
    cursor.close()

def fname1():
# 查询数据
    conn = sqlite3.connect(DBname)
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM pymoo')
# 获取查询结果
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def Close():
    conn = sqlite3.connect(DBname)
    conn.close()


# 提交更改
#conn.commit()
# 关闭游标
#cursor.close()

#conn.close()