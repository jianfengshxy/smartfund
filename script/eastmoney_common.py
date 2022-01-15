# -*- encoding=utf8 -*-
__author__ = "shixiaoyu"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
import mysql.connector

# if not cli_setup():
#     auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/SJE0217722000066?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH",], project_root="/Users/shixiaoyu/Downloads/OneDrive/App_monitor.air")

mydb = mysql.connector.connect(
# host="rm-uf61u0rh46akeoy6eyo.mysql.rds.aliyuncs.com",       # 数据库主机地址
  host="rm-uf61u0rh46akeoy6eyo.mysql.rds.aliyuncs.com",
  user="jianfengshxy",    # 数据库用户名
  database="smartfund",  #数据库
  passwd="sWX15706"   # 数据库密码
)

mycursor = mydb.cursor()


# script content
def demo():
    print("start...demo")
    sleep(1)

    

def print_db():
  mycursor = mydb.cursor()
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    print(x)  
    
def get_result():
    sql = "SELECT * FROM fund_570001 limit 100"
    mycursor.execute(sql)
    return   mycursor.fetchall()
