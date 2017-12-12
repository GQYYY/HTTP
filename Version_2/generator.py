#!/usr/bin/env python
# coding=utf-8

import http_request
import utils
import socket
import time


class Generator:
    '''
    解析、生成、测试HTTP Requst的操作类
    '''
    def __init__(self, network_path=None, network=None):
        
        self.request = http_request.Request()   #Request类的对象
        self.network_path = network_path
        self.network = network
        
        self.attack_html = '<!DOCTYPE html>\n<html>\n<head>\n<title>Attack!</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>This is www.attack.com!</h1>\n<h1>You have been hacked!</h1>\n\n\n<p><em>You have been hacked!</em></p>\n</body>\n</html>\n'
        self.benigh_html = '<!DOCTYPE html>\n<html>\n<head>\n<title>Benigh!</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>Welcome to www.benigh.com!</h1>\n\n<p><em>Thank you for logining in www.benigh.com!</em></p>\n</body>\n</html>\n'
        self.bad_request_html = '<html>\r\n<head><title>400 Bad Request</title></head>\r\n<body bgcolor="white">\r\n<center><h1>400 Bad Request</h1></center>\r\n<hr><center>nginx/1.13.6</center>\r\n</body>\r\n</html>\r\n'
        
    
    def conf_parse(self,conf_path,conf_file):
        '''
        解析路径conf_path下的带有配置选项的文件conf_file,并给self.request的各属性赋值,如:
        * self.request.Headers
        * self.request.Request_Line
        * self.request.Header_Line_CRLF
        * self.request.End_Line
        '''

        conf_dict = utils.load(conf_path+conf_file)
        '''
        conf_dict中每个key对应的value的type有三种取值情况:
        * value是字符串列表，如 "Header_Line_CRLF": ["\r\n"]
        * value是dict
        * value是dict的列表
        '''
        for key,values in conf_dict.items():
            func = getattr(self.request,key.lower())

            #key对应的值是dict
            if isinstance(values,dict):
                func(**values)
            #key对应的值是列表
            elif isinstance(values,list):
                for value in values:
                    #列表中的元素是dict
                    if isinstance(value,dict):
                        func(**value)
                    #列表中的元素不是dict，可能是数字、str或list
                    else:
                        #注意:这里不是程序解包，是位置参数
                        func(values)
                        break   
                        
                        
    def get_request(self):
        '''
        wrapper function
        返回self.request中所有可能的HTTP Request的字符串表示
        '''
        return self.request.get_request()
    
    
    def get_response(self,requests,target_host,target_port):
        '''
        返回HTTP Response列表
        requests是一个HTTP请求的列表
        逐一从requests中取出Request,并发送给target_host:target_port
        得到的resonse逐一添加到一个列表中并返回
        '''
        response_lst = []
        #建立一个socket对象
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #客户端链接服务器端
        client.connect((target_host,target_port))

        for request in requests:
            #把str类型的request转成bytes类型
            request = bytes(request,encoding='utf-8')
            #发送数据
            client.send(request)
            #接收服务器返回的resonse,此时response是bypes类型
            response = client.recv(4096)
            #将bytes类型转成str
            response = bytes.decode(response)
            response_lst.append(response)
            time.sleep(1)
        return response_lst
    
    
    def network_test(self,requests):
        '''
        解析网络配置文件，并将requests列表中的请求逐一发给由网络配置文件设置的各个server工具，
        并进行differential testing
        '''
        raw_result = {}
        servers = utils.load(self.network_path+self.network).get('server')
        #对各个server进行differential testing
        for server in servers:
            raw_result[server.get('name')] = self.get_response(requests,
                                                           server.get('host'),server.get('port'))
        
        #分析各个server的结果是否一致
        result = {}
        for server_name,response_lst in raw_result.items():
            result[server_name] = []
            for response in response_lst:
                headers,message_body = response.split('\r\n\r\n')
                status_code = headers.split('\r\n')[0]
                
                if message_body == self.attack_html:
                    html_content = 'attack.html'
                elif message_body == self.benigh_html:
                    html_content = 'benigh.html'
                elif message_body == self.bad_request_html:
                    html_content = 'bad_request.html'
                else:
                    html_content = 'other'
                
                result[server_name].append((status_code,html_content))
            print (server_name ,':',result.get(server_name))
            print ('\n')
            
        return raw_result,result
        
    
   
