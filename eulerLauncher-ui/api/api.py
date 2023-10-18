#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 17:01:39
LastEditTime: 2023-05-30 15:41:05
Description: 业务层API，供前端JS调用
usage: 在Javascript中调用window.pywebview.api.<methodname>(<parameters>)
'''

from api.storage import Storage
from api.system import System
import json
import re
import os
class EUAction:
    def __init__(self):
        pass
        # 判断eulerlauncher是否正常运行，是否可以使用。读取可执行程序的路径。
        # 也可以做一个判断函数，每次函数调用前都使用。
    def run(self,command,wait=True):
        p = os.popen(command)
        print(p)
        if wait:
            result = p.read()
            return result
        else:
            return p
        # python与命令行的交互
eu = EUAction()
class API(System, Storage):
    '''业务层API，供前端JS调用'''

    def setWindow(self, window):
        '''获取窗口实例'''
        System.window = window
    def ttt(self):
        print(1)
        return 5
    def getImageList(self):
        imagesText = eu.run('eulerlauncher images')

        imagesTextList = re.findall(r'\|(.+?)\|(.+?)\|(.+?)\|', imagesText)
        images = []
        # 打印匹配结果
        for imageText in imagesTextList:
            image_name, location, status = [s.strip() for s in imageText]
            if image_name == 'Images':
                continue
            images.append({"name": image_name, "location": location, "status": status})
        print(images)
        return images
    def downloadImage(self,imageName):
        print(11222)
        try:
            print(1111111)
            eu.run('eulerlauncher download-image %s' % imageName,wait=False)
            print(111)
            return True
        except Exception as e:
            return False
        # 这个函数不返回成功或失败信息，又前端调用getImageList查看状态
        # 可能会有问题，下载的命令占用着，无法执行其它命令，需要调试。
    def loadLocalImage(self,fileList):
        # 满足格式：.qcow2.xz,.qcow2
        try:
            results = []
            for file in fileList:
                path = file['path']
                cut_name = file['filename'].split('.')[0]
                results.append(eu.run(f'eulerlauncher load-image --path {path} {cut_name}'))
            print(results)
            return results
        except Exception as e:
            return True
        # 这里会有文件操作嘛？
    def deleteImage(self,name):
            # 满足格式：.qcow2.xz,.qcow2
        result = eu.run(f'eulerlauncher delete-image {name}')
        print(result)
        # 如何判断成功执行
        return result



    # instance虚拟机操作
    def getInstanceList(self):
        insText = eu.run('eulerlauncher list')

        insTextList = re.findall(r'\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|', insText)
        ines = []
        # 打印匹配结果
        for insText in insTextList:
            name, image_name, state, ip = [s.strip() for s in insText]
            if image_name == 'Images':
                continue
            ines.append({"name": name,'image':image_name, "state": state, "ip": ip})
        print(ines)
        return ines
    def createInstance(self,image,name):
        result = eu.run(f'eulerlauncher launch --image {image} {name}')
        return result
    def deleteInstance(self,name):
        result = eu.run(f'eulerlauncher delete-instance {name}')
        return result
        
    
