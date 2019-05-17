#coding=utf-8
import os
import time
LOG_DIRECTORY = "./"
class Print(object):
    @staticmethod
    def info(message):
        out_message =  Print.timeStamp() + '  ' + 'INFO: ' +str(message)
        Print.write(out_message)
        print(out_message)

    @staticmethod
    def write(message):
        log_path = os.path.join(LOG_DIRECTORY, 'log.txt')
        with open(log_path,'a+') as f:
            f.write(message)
            f.write('\n')

    @staticmethod
    def timeStamp():
        local_time = time.localtime(time.time())
        return time.strftime("%Y_%m_%d-%H_%M_%S", local_time)

if __name__ == '__main__':
    print(Print.timeStamp())
    Print.info("hello world")