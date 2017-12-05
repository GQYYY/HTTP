#!/usr/bin/env python
# coding=utf_8

class Request:
    def __init__(self,Method='GET',Request_URI='/',HTTP_Version='HTTP/1.1'):
        self.Line_CRLF = '\r\n'
        self.Headers = [] #其中的内容是一个一个(header_name,header_value)的元组
        self.Method = Method
        self.Requset_URI = Request_URI
        self.HTTP_Version = HTTP_Version

    '''
    向request中添加Header信息，以元组表示(header_name,header_value),参数如下:
    header_name: Header名，连同后面的冒号(:),如 'Host:'等
    header_value:该Header对应的值
    header_style:该Header在此Header_Line中的style，其值可以是['None'(默认),'space_preceded','space_succeeded'],以Host字段为例:
        'None' --> 'Host:value'
        'space_preceded' --> ' Host:value'
        'space_succeeded' --> 'Host: value'
    '''
    def set_Header(self,header_name,header_value,header_style=None):
        if header_style == 'space_preceded':
            header_name = ' ' + header_name + ':'
        elif header_style == 'space_succeeded':
            header_name = header_name + ':' + ' '
        else: 
            header_name = header_name + ':'
        
        self.Headers.append((header_name,header_value))
    
    
    '''返回该Request的字符串表示'''
    def request(self):
        Request_Line = self.Method +' '+ self.Requset_URI +' '+ self.HTTP_Version + self.Line_CRLF
        End_Line = self.Line_CRLF
        Header_Lines = ''

        for header in self.Headers:
            Header_Line = header[0]+header[1]+self.Line_CRLF
            Header_Lines += Header_Line

        return ''.join([Request_Line,Header_Lines,End_Line])
    
    def clear_headers(self):
        self.Headers = []

