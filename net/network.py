#-*- coding:utf8 -*-

import sys
import datetime
import numpy as np
import pandas as pd
from pyecharts import Graph
sys.path.append('../my/')
from db import pool
from const import *


def pearson(X, Y):
	'''
	皮尔逊相关系数
	要求:
	X与Y必须等长
	X、Y允许有缺失值
	'''
	r = X.corr(Y, method='pearson')
	return r if r is not np.nan else 0.
	

class NetWork(object):
	def __init__(self, sday, eday, method='volume', distance=pearson):
		'''
		method:
		volume			使用总成交量的时间序列距离建立权值
		return_rate		使用主力合约对数收益率的时间序列距离建立权值
		same_day_open	使用用户行为建立权值，若用户同天开仓两个品种，则权值加一
		same_day_drop	使用用户行为建立权值，若用户同天平仓两个品种，则权值加一
		same_day_hold	使用用户行为建立权值，若用户同天持仓两个品种，则权值加一
		
		sday, eday:
		时间窗的左右边界
		
		distance:
		仅对于使用时间序列的建图的方法有效，此处应给定一个函数，用来计算两个时间序列的距离
		'''
		# method的范围约束
		assert method in ['volume', 'return_rate', 'same_day_open', 'same_day_drop', 'same_day_hold']
		# 时间窗约束
		assert datetime.date(2014,1,1) <= sday <= eday <= datetime.date(2016,12,31)
		# 链接数据库
		conn = pool.dedicated_connection()
		cursor = conn.cursor()
		# 时间窗内交易的品种
		sql = "select distinct code from commodity.contract_daily where date between %s and %s"
		cursor.execute(sql, (sday,eday))
		codes = [row[0] for row in cursor.fetchall()]
		self.codes = codes
		# 时间序列类方法
		if method in ['volume', 'return_rate']:
			data = []
			cursor.execute("use commodity")
			if method=='volume':
				sql = "select volume from (select day from trade_day where day between %s and %s) as tmp1 \
				left join \
				(select date,sum(volume) as volume from contract_daily where code=%s and date between %s and %s group by date) as tmp2 \
				on day=date order by date asc"
			else:
				sql = "select settle from trade_day left join \
				(select date,settle from main_contract where code=%s) as tmp \
				on day=date where day between %s and %s order by date asc"
			# 查询序列数据
			for code in codes:
				cursor.execute(sql, (sday, eday, code, sday, eday))
				data.append([row[0] for row in cursor.fetchall()])
			df = pd.DataFrame(data, dtype=np.float64)
			# 初始化邻接矩阵
			mat = np.zeros([len(codes), len(codes)])
			self.mat = mat
			# 计算邻接矩阵
			for i in range(len(codes)):
				for j in range(i+1, len(codes)):
					mat[i,j] = distance(df.iloc[i], df.iloc[j])
					mat[j,i] = mat[i,j]
		else:
			pass
		
	def graph(self):
		V = [{'name':code2name[c]} for c in self.codes]
		E = []
		for i in range(len(self.codes)):
			for j in range(i+1, len(self.codes)):
				if abs(self.mat[i,j])>=0.7:
					E.append({'source':i, 'target':j, 'value':round(self.mat[i,j],3)})
		graph = Graph(width=1000, height=618)
		graph.add("", V, E, graph_layout='force', graph_repulsion=1000, line_curve=0.2, is_label_show=True)
		return graph
		pass

if __name__=='__main__':
	net = NetWork(datetime.date(2014,1,1), datetime.date(2014,1,10))
	net.graph().render()
