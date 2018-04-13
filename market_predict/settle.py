#-*- coding:utf8 -*-

'''
使用过去N天的结算价、成交量、持仓量，预测第N+1天结算价
'''

import pymysql
import tensorflow as tf

conn = pymysql.connect(host="219.224.169.45", user="lizimeng", password="codegeass", db="market")
cursor = conn.cursor()

sql = "select * from contract_daily where "

cursor.close()
conn.close()
