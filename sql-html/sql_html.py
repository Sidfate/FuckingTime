#!/usr/bin/env python    
#encoding: utf-8  
import sys     
import MySQLdb
from pyh import *

reload(sys)
sys.setdefaultencoding('utf8')

config = {
	'host': '',
	'user': '',
	'passwd': '',
	'port': 3306,
	'charset': 'utf8',
	'database': ''
}
database = config['database']

try:
	#数据库连接
	conn = MySQLdb.connect(host=config['host'], user=config['user'], passwd=config['passwd'], port=config['port'], charset=config['charset'])
	cur = conn.cursor()

	#选择数据库
	conn.select_db(database)

	#获取表名列表
	cur.execute("SELECT TABLE_NAME, TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '" + database + "' ORDER BY TABLE_NAME ASC")
	tables = cur.fetchall()

	"""
		table_fields 字典：存放各个表的字段信息
			key:表名
			value:字段信息列表
	"""
	table_fields = dict()
	table_comment = dict()
	for t in tables:
		cur.execute("show full columns from " + t[0])
		fields = cur.fetchall()
		table_comment[t[0]] = t[1] 
		table_fields[t[0]] = fields             
	
except MySQLdb.Error, e:
	print "Mysql Error %d: %s" % (e.args[0], e.args[1])
	exit()

#创建css文件
file_obj = open('index.css', 'w')
file_obj.write("""
        body
        {
            font-size: 9pt;
        }
        .table 
        {
        	margin:0 auto;
        }
        .styledb
        {
            font-size: 14px;
        }
        .styletab
        {
            font-size: 14px;
            padding-top:15px;             
        }
    """)
file_obj.close()

#pyh库创建html文件
page = PyH('数据库 ' + database + ' 结构')
page.addCSS('index.css')
main = page << div(style='text-align: center')
main << div('数据库名: '+ database, cl='styledb')
for table_name in sorted(table_fields.keys()):
	fields = table_fields[table_name]

	comment = ''
	if table_comment[table_name]:
		comment = '(' + table_comment[table_name] + ')'
	main << div('表名:' + table_name + comment, cl='styletab')
	main << div(align='left')
	_div = main << div()
	_table = _div << table(border='0', cellpadding='5', width='90%', cl='table') << tr() << td(bgcolor='#FBFBFB') << table(cellspacing="0",cellpadding="5",border="1",width="100%",bordercolorlight="#D7D7E5",bordercolordark="#D3D8E0")
	_table << tr(bgcolor='#F0F0F0') << td('名字')+td('类型')+td('排序方式')+td('空')+td('键')+td('默认')+td('额外')+td('注释')
	for field in fields:
		_tr = _table << tr()
		for f in field:
			if field.index(f) == 7:
				continue
			_tr << td(f)
		
page.printOut(database + '.html')




