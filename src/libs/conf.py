#coding: utf8
'''
==========================================================================================
Created on 2020-11-19 15:30:55
@author: Simon
==========================================================================================
'''
from multiprocessing import Manager

class GlobalConf():
    Log = None
    

# class JobManager():
#     Log = None
#     idx = 0
#     status = {}
#     progress = {}
#
#     @staticmethod
#     def add_job(url=None):
#         num = JobManager.idx = JobManager.idx + 1
#         JobManager.progress[num] = []
#         JobManager.status[num] = 0
#         print("create job :", num)
#         return num


class GlobalData():
    # idx = 0
    # mg = Manager()
    # jobs = mg.dict()
    # idx = mg.Value(0)
    mg = None
    jobs = None
    idx = None
    
    @staticmethod
    def get_id():
        GlobalData.idx += 1 
        return GlobalData.idx
    
        
    
if __name__ == '__main__':
    pass