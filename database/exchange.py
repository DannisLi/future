# -*- coding:utf8 -*-

import pymysql

vari2exchange = {
'a' : 'dce',
'ag' : 'shfe',
'al' : 'shfe',
'ap' : 'czce',
'au' : 'shfe',
'b' : 'dce',
'bb' : 'dce',
'bu' : 'shfe',
'c' : 'dce',
'cf' : 'czce',
'cs' : 'dce',
'cu' : 'shfe',
'cy' : 'czce',
'er' : 'czce',
'fb' : 'dce',
'fg' : 'czce',
'fu' : 'shfe',
'hc' : 'shfe',
'i' : 'dce',
'ic' : 'cffex',
'if' : 'cffex',
'ih' : 'cffex',
'j' : 'dce',
'jd' : 'dce',
'jm' : 'dce',
'jr' : 'czce',
'l' : 'dce',
'lr' : 'czce',
'm' : 'dce',
'ma' : 'czce',
'me' : 'czce',
'ni' : 'shfe',
'oi' : 'czce',
'p' : 'dce',
'pb' : 'shfe',
'pm' : 'czce',
'pp' : 'dce',
'rb' : 'shfe',
'ri' : 'czce',
'rm' : 'czce',
'ro' : 'czce',
'rs' : 'czce',
'ru' : 'shfe',
'sf' : 'czce',
'sm' : 'czce',
'sn' : 'shfe',
'sr' : 'czce',
't' : 'cffex',
'ta' : 'czce',
'tc' : 'czce',
'tf' : 'cffex',
'v' : 'dce',
'wh' : 'czce',
'wr' : 'shfe',
'ws' : 'czce',
'y' : 'dce',
'zc' : 'czce',
'zn' : 'shfe'
}

conn = pymysql.connect(host='219.224.169.45', user='lizimeng', password='codegeass', db='market', charset='utf8')
cursor = conn.cursor()

sql = "insert into exchange (vari,exchange) values (%s,%s)"
for vari in vari2exchange.keys():
	cursor.execute(sql, (vari, vari2exchange[vari]))
conn.commit()

cursor.close()
conn.close()
