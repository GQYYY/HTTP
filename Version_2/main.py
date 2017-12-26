#!/usr/bin/env python
# coding=utf-8

import argparse
import generator
from texttable import Texttable

#添加命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('rule',metavar='rule',nargs='+',help='specify the file name of rule configuration(.conf)')
parser.add_argument('-rp','--rule-path',metavar='rule_path',
                    help='specify the path of rule configuration files',
                    default='/home/gqy/Desktop/Http_Gengerator/Version_2/config/rules/')
parser.add_argument('-g','--grammar',metavar='grammar',
                    help='specify the file name of rule configuration(.conf)',
                    default='grammar.conf')
parser.add_argument('-gp','--grammar-path',metavar='grammar_path',
                    help='specify the path of grammar configuration files',
                    default='/home/gqy/Desktop/Http_Gengerator/Version_2/config/grammars/')
parser.add_argument('-np','--network-path',metavar='network_path',
                    help='specify the path of network environment configuration files',
                    default='/home/gqy/Desktop/Http_Gengerator/Version_2/config/network-env/')
parser.add_argument('-n','--network',metavar='network',
                    help='specify the file name of network environment configuration(.conf)',
                    default='network.conf')

#解析命令行参数
args = parser.parse_args()

generator = generator.Generator(network_path=args.network_path, network=args.network)

#分别解析Grammar文件和Rule文件
generator.conf_parse(args.grammar_path,args.grammar)
for rule in args.rule:
    generator.conf_parse(args.rule_path,rule)


#得到所有可能的HTTP Request的字符串表示
requests = generator.get_request()

print ('所生成的Request如下:\n')
for index,request in enumerate(requests,1):
    print('第%d个:'%(index))
    print(request)

#结果展示与对比
print ('测试结果如下:\n')
#用得到的requests对所有的待测工具进行Differential Testing
raw_result, result = generator.network_test(requests)

keys = list(result.keys())
values = list(result.values())

table = Texttable()
table.set_deco(Texttable.HEADER)

#设置每列的数据类型，均为text
cols_dtype = ['t']*(len(keys)+1)
table.set_cols_dtype(cols_dtype)    

#设置每列的对齐方式
cols_align = ['c']
cols_align.extend(['r']*len(keys))
table.set_cols_align(cols_align)

rows = []
table_header_line = [u'Test Case\n ID']    #表头行
table_header_line.extend(keys)
rows.append(table_header_line)

for j in range(len(values[0])):   #对所有的test case的编号进行遍历
    row = [j+1]
    for i in range(len(values)):  #对所有的key的编号进行遍历
        row.append(values[i][j])
    rows.append(row)
    
table.add_rows(rows)
print (table.draw()+'\n')
