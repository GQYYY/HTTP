#!/usr/bin/env python
# coding=utf-8

import argparse
import generator

#添加命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('rule',metavar='rule',help='specify the file name of rule configuration(.conf)')
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
generator.conf_parse(args.rule_path,args.rule)


#得到所有可能的HTTP Request的字符串表示
requests = generator.get_request()

print ('所生成的Request如下：')
for request in requests:
    print(request)

print ('测试结果如下：')
#用得到的requests对所有的待测工具进行Differential Testing
raw_result, result = generator.network_test(requests)