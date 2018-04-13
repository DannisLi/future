# -*- coding:utf8 -*-

import pymysql

vari2name = {
'a' : '豆一',
'ag' : '沪银',
'al' : '沪铝',
'ap' : '苹果',
'au' : '沪金',
'b' : '豆二',
'bb' : '胶合板',
'bu' : '沥青',
'c' : '玉米',
'cf' : '郑棉',
'cs' : '玉米淀粉',
'cu' : '沪铜',
'cy' : '棉纱',
'er' : '早籼稻(ER)',
'fb' : '纤维板',
'fg' : '玻璃',
'fu' : '燃油',
'hc' : '热轧卷板',
'i' : '铁矿石',
'ic' : '中证500指数',
'if' : '沪深300指数',
'ih' : '上证50指数',
'j' : '焦炭',
'jd' : '鸡蛋',
'jm' : '焦煤',
'jr' : '粳稻',
'l' : '塑料',
'lr' : '晚籼稻',
'm' : '豆粕',
'ma' : '甲醇(MA)',
'me' : '甲醇(ME)',
'ni' : '沪镍',
'oi' : '菜油(OI)',
'p' : '棕榈油',
'pb' : '沪铅',
'pm' : '普麦',
'pp' : '聚丙烯',
'rb' : '螺纹钢',
'ri' : '早籼稻(RI)',
'rm' : '菜粕',
'ro' : '菜油(RO)',
'rs' : '菜籽',
'ru' : '橡胶',
'sf' : '硅铁',
'sm' : '锰硅',
'sn' : '沪锡',
'sr' : '白糖',
't' : '10年期国债',
'ta' : 'PTA',
'tc' : '动力煤(TC)',
'tf' : '5年期国债',
'v' : 'PVC',
'wh' : '强麦(WH)',
'wr' : '线材',
'ws' : '强麦(WS)',
'y' : '豆油',
'zc' : '动力煤(ZC)',
'zn' : '沪锌'
}

conn = pymysql.connect(host='219.224.169.45', user='lizimeng', password='codegeass', db='market', charset='utf8')
cursor = conn.cursor()

sql = "insert into vari_name (vari,name) values (%s,%s)"
for vari in vari2name.keys():
	cursor.execute(sql, (vari,vari2name[vari]))
conn.commit()
cursor.close()
conn.close()