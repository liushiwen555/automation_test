# coding = utf-8
# Author: ZhaoGe
# Date: 2021/5/23 14:18


import logging
import traceback

class SetLog(object):
    def __init__(self,file='/Users/liushiwen/PycharmProjects/my_web_ui_project/logs/logtest.log'):
        self.file = file
        '''创建日志器'''
        self.log = logging.getLogger()
        '''日志器设置日志级别'''
        self.log.setLevel(logging.DEBUG)

    def setFormatter(self):
        '''
        设置格式器
        :return: tuple
        '''
        self.formatter1 = logging.Formatter(fmt="%(asctime)s ==> %(filename)s ==> %(levelname)s ==> %(message)s")
        self.formatter2 = logging.Formatter(fmt="%(asctime)s : %(filename)s : %(levelname)s : %(message)s")
        return self.formatter1,self.formatter2

    def setStreamHandle(self):
        '''创建控制台处理器,将控制台处理器添加进日志器,控制台处理器设置日志级别,设置日志打印格式'''
        stream_handle=logging.StreamHandler()
        self.log.addHandler(stream_handle)
        stream_handle.setLevel(logging.DEBUG)
        stream_handle.setFormatter(self.setFormatter()[0])

    def setFileHandle(self):
        '''
        创建文件处理器，将文件处理器添加进格式器，给文件处理器添加日志输出格式，给文件处理器设置日志输出级别
        :param file: file name
        :return:
        '''
        filehandle = logging.FileHandler(filename=self.file,mode="a",encoding="utf-8")
        self.log.addHandler(filehandle)
        filehandle.setFormatter(self.setFormatter()[1])
        filehandle.setLevel(logging.INFO)

    def get_logger(self):
        '''
        返还日志器
        :param file:
        :return:
        '''
        self.setStreamHandle()
        self.setFileHandle()
        return self.log


if __name__ == '__main__':
    logger = SetLog().get_logger()
    def func(num1,num2):
        try:
            num_sum = num1 * num2
            print(num_sum)
        except BaseException as e:
            logger.error(traceback.format_exc())

    func(1,2)
    func("hello","python")