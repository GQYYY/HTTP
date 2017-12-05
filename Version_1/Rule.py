#!/usr/bin/env python
# coding=utf-8

import json
import itertools


class Rule:
    def __init__(self,rule_filename):
        self.rule_path = '/home/gqy/Desktop/Http_Gengerator/Version_1/'
        self.default_header_copy_num = 0
        self.default_header_style = None

        self.rule = self.load_rule(rule_filename)

    '''
    从.conf文件中加载rule信息
    rule信息由json格式表示
    返一个dict
    '''
    def load_rule(self,rule_filename):
        rule = None
        with open(self.rule_path+rule_filename,'r') as f:
            rule = json.load(f)
        return rule
    

    '''
    解析得到该rule有多少种对应的形式
    返回值是一个dict: {header-name:header-style}
    其中，header-style是一个列表，包含该header的所有style组合
    '''
    def get_rule(self):
        rules = {}
        if self.rule.get('header_copy'):
            for header in self.rule.get('header_copy'):
                header_style = [None]*header.get('num')
                if header.get('header_style'):
                    header_style = header.get('header_style')
                    header_style.extend([self.default_header_style]*(header.get('num')-len(header.get('header_style'))))
                #得到该header的所有style的组合
                header_style = list(set(list(itertools.permutations(header_style,len(header_style)))))
                rules[header.get('header_name')] = header_style
        return rules
