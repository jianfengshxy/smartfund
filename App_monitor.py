# -*- encoding=utf8 -*-
__author__ = "shixiaoyu"

import sys,getopt
sys.path.append('./script')

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import time  # 引入time模块
import re
from eastmoney_common  import *





def login_to_main(username,password): 
    # # #保证环境为初始化状态，如果前面操作过App，退出天天基金App
    stop_app("com.eastmoney.android.fund")
    # 启动天天基金App
    start_app("com.eastmoney.android.fund")

    if(poco("com.eastmoney.android.fund:id/tv_full_screen_privacy_comfirm").wait(5).exists()):
         poco("com.eastmoney.android.fund:id/tv_full_screen_privacy_comfirm").click()

    
    
    #等待开屏广告10秒，再去主页点击“我的”按钮
    if(poco("com.eastmoney.android.fund:id/btn_tab_txt_5").wait(10).exists()):
            poco("com.eastmoney.android.fund:id/btn_tab_txt_5").click()
   
    #系统维护
    if(poco("com.eastmoney.android.fund:id/dialog_btn_two").exists()):
             poco("com.eastmoney.android.fund:id/dialog_btn_two").click()
             sys.exit()

    #如果App上次操作账户安全退出，下一次打开从主页“我的”按钮，进入"登录 / 开户"
    if(poco("登录 / 开户").wait(5).exists()):
            poco("登录 / 开户").click()
    
    #如果App上次操作账户没有退出，直接将上一次登录账户带入到登录页面
    #如果是重新安装，需要选择账户登录
    if(poco("com.eastmoney.android.fund:id/f_dialog_account_login").exists()):
          poco("com.eastmoney.android.fund:id/f_dialog_account_login").click()
    #############
    poco("com.eastmoney.android.fund:id/edittext_username_2").set_text("321111198405315315")
    poco("com.eastmoney.android.fund:id/edittext_password_2").set_text("sWX15706")
    poco("com.eastmoney.android.fund:id/button_login").click()
    sleep(1)
    #-----------------------------------------------------------------------------------------------

    #初次安装要跳过手势密码设置
    if(poco("com.eastmoney.android.fund:id/tips").exists()):
            poco("com.eastmoney.android.fund:id/jump").click()
            poco("com.eastmoney.android.fund:id/dialog_btn_two").click()
        
    #从用户账户管理页面返回个人主页,验证是否登录成功
#     if(poco("com.eastmoney.android.fund:id/pass_portrait").exists()):
#         print("login failed!")
#     else:
#         print("login success!")
#         sleep(1)


    
    

def fund_group(group_name):
    # 进入“组合”页面
    if(poco("组合").wait(30).exists()):
         poco("组合").click()
            
    while(not poco(group_name).wait(5).exists() and not poco("了解组合").exists()):
         poco("android.widget.ScrollView").swipe('up')
         poco("android.widget.ScrollView").swipe('up')
     
    #####有可能基础账户不存在，
    if(poco(group_name).exists()):
            poco(group_name).click() 
 
    
              
 
def  sell_group_fund(group_name):  
    
#####可能账户不存在，没进入组合页面，直接退出
    if(not poco("group_name").exists()):
                          return
# 记录已经处理的基金，因为赎回基金后回跳出组合，导致没有办法在原来的顺序上继续，
# 必须记录已经处理过的基金，加快速度
#
    handled_fund = ()
    to_end = False
    sell_exit = True
    while(sell_exit):
        while(not to_end):
           to_end = poco("已经到底了").exists() 
            
           if(poco("累计收益").wait(10).exists()  and  poco("全部产品").wait(10).exists()):
                  poco.swipe(poco("全部产品").get_position(),poco("累计收益").get_position())
       
           print("&&&&&&&&&&&&&&&&&&&&&&&")    

           for i in poco(nameMatches="[0-9][0-9][0-9][0-9][0-9][0-9]"):
                fund_code = i.get_name()
                if(fund_code in handled_fund):
                          #####移动基金组合页面进行遍历  
                          x1,y1=poco("androidx.recyclerview.widget.RecyclerView").get_size()
                          poco("androidx.recyclerview.widget.RecyclerView").swipe([-x1/2,-y1/2])     
                          ########################### 
                          sell_exit = False
                          continue
         
            ##### 进入基金持有页面
                sleep(3)
                print("基金代码:" + fund_code)
                poco(fund_code).wait(30).click()   
                
                
       ####更新数据库数据
       
    
    
       ####结束更新        
       ##### 如果基金不支持赎回，直接跳过
                if(poco("暂停赎回").exists()):
                         print("暂停赎回")
                         poco(name="com.eastmoney.android.fund:id/nav_tv").wait_for_appearance(60)
                         poco(name="com.eastmoney.android.fund:id/nav_tv").click()
                         handled_fund = handled_fund + (fund_code,) 
                         sell_exit = False
                         continue
       ##### 如果基金可用份额为0.0，直接跳过    
                if(poco("0.00").wait(5).exists()):
                        poco(name="com.eastmoney.android.fund:id/nav_tv").wait_for_appearance(60)
                        poco(name="com.eastmoney.android.fund:id/nav_tv").click()
                        handled_fund = handled_fund + (fund_code,)
                        sell_exit = False
                        continue          
                hold_rate = poco(nameMatches="[+-]*\d*\.\d*%")[2].get_name()
                print("持有收益率" + hold_rate.replace("%",""))     
                ####这里应该课配置，读取数据库获取实时止盈比例
                if( float(hold_rate.replace("%","")) > 3.0):    
                       poco("卖出/转换").wait(30).click()
                       if(group_name != "基础账户资产"):
                             poco(group_name).wait(30).click()                     
                             poco("从组合中卖出").wait(30).click()
                       poco("回活期宝").wait(30).click()
                       if(poco("该基金交易规则特殊，暂不支持极速赎回充值活期宝。").exists()):
                            poco("普通").wait(30).click() 
                       else:
                            poco("极速").wait(30).click()
                              

                       poco("全部").wait(30).click()
                       if(poco("同意协议并提交").exists()):
                            poco("同意协议并提交").click()
                       if(poco("继续卖出").wait(10).exists()):
                                poco("继续卖出").click()
                       if(poco("确认").exists()):
                              poco("确认").click()
                       poco("com.eastmoney.android.fund:id/et_pwd").wait(10).set_text("sWX15706")
                       poco("com.eastmoney.android.fund:id/btn_comfirm").wait(10).click()
                       poco(text="完成").click()
                       handled_fund = handled_fund + (fund_code,)                                          
                       to_end = False
                       sell_exit = True
                       fund_group(group_name)
                       break
                else:                                      
                      ##返回基金组合页面
                       sell_exit = False
                       handled_fund = handled_fund + (fund_code,) 
                       poco(name="com.eastmoney.android.fund:id/nav_tv").wait_for_appearance(60)
                       poco(name="com.eastmoney.android.fund:id/nav_tv").click()   
                       ################                        
                       #####移动基金组合页面进行遍历  
#                        print("159 sell_exit " + str(sell_exit))
                       x1,y1=poco("androidx.recyclerview.widget.RecyclerView").get_size()
                       poco("androidx.recyclerview.widget.RecyclerView").swipe([-x1/2,-y1/2])       
                       ########################### 
        

def buy_group_fund():        
    
    # 点击“买入”
    poco("买入").wait(30).click()
    #确定进入搜索矿
    poco("android.widget.EditText").click()
    poco("android.widget.EditText").set_text("005702")
    poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("com.eastmoney.android.fund:id/mini_fragment_container_id").offspring("com.eastmoney.android.fund:id/container").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[2].child("android.widget.FrameLayout").offspring("androidx.recyclerview.widget.RecyclerView").child("android.widget.FrameLayout")[0].child("android.widget.FrameLayout")[0].child("android.widget.FrameLayout").click()
    sleep(2)

    poco("android.widget.LinearLayout").offspring("com.eastmoney.android.fund:id/mini_fragment_container_id").child("android.widget.FrameLayout").offspring("com.eastmoney.android.fund:id/container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[0].offspring("android.widget.ScrollView").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[1].child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[1].child("android.widget.FrameLayout").child("android.widget.FrameLayout")[0].click()
    sleep(1)
    poco("com.eastmoney.android.fund:id/pop_fragment_container").offspring("com.eastmoney.android.fund:id/container").child("android.widget.FrameLayout").offspring("androidx.viewpager.widget.ViewPager").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[1].offspring("android.widget.ScrollView").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[0].child("android.widget.FrameLayout")[0].child("android.widget.FrameLayout").child("android.widget.FrameLayout")[1].child("android.widget.FrameLayout").offspring("可用余额：").click()
    poco("android.widget.EditText").set_text(10)

    ensure_btn=poco("android.widget.LinearLayout").offspring("com.eastmoney.android.fund:id/mini_fragment_container_id").child("android.widget.FrameLayout").offspring("com.eastmoney.android.fund:id/container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[1].child("android.widget.FrameLayout").child("android.widget.FrameLayout")[0].offspring("android.widget.ImageView")

    poco("确定买入").click()
    poco("com.eastmoney.android.fund:id/et_pwd").set_text("sWX15706")

    poco("com.eastmoney.android.fund:id/iv_eye")
    if(poco("com.eastmoney.android.fund:id/btn_comfirm").attr("enabled")):
            poco("com.eastmoney.android.fund:id/btn_comfirm").click()
    sleep(3)
    poco(text="完成").click()
    sleep(3)
    poco("android.widget.LinearLayout").offspring("com.eastmoney.android.fund:id/mini_fragment_container_id").offspring("com.eastmoney.android.fund:id/container").child("android.widget.FrameLayout").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[0].child("android.widget.FrameLayout").offspring("android.widget.ImageView")[0].click()

    
def bussiness_logic(username,password): 
    print("bussiness_logic")
# ####输入用户名密码，从开启APP到登录到个人资产页面
    login_to_main(username,password)
# ###################扫描账户，及时赎回
# # 进入基金
    if(poco("基金").wait(30).exists()):
        poco("基金").click()  
    fund_group("基础账户资产")
#     sell_group_fund("基础账户资产")

# ##卖完基金，无发确定终点，直接重启App进入购买流程
# ####输入用户名密码，从开启APP到登录到个人资产页面
#     login_to_main("321111198405315315","sWX15706")
#     poco.swipe([0.1574074074074074, 0.8197916666666667],[0.4537037037037037, 0.1421875])
#     buy_group_fund()    

device_url="SJE0217722000066"

if(len(sys.argv) > 4):
    device_url = sys.argv[4]
#     print("device_url:" + device_url)
    
#在用户表中用户和设备ID绑定 
device_id = re.sub(r'\?.*$',"", device_url.split('/')[-1]).split("?")[0]



auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/"+device_id+"?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH",], project_root="/Users/shixiaoyu/Downloads/OneDrive/App_monitor.air")
#auto_setup(__file__,devices=["android://127.0.0.1:5037/127.0.0.1:SJE0217722000066"])
# auto_setup(__file__)
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)    
        
#########
###查询数据库找出所有用户，进行遍历业务处理
#########    
# print_db() 
for x in get_result():    
     print(x)

bussiness_logic("321111198405315315","sWX15706")


