#coding: utf8
'''
==================================================================
Created on 2021年12月13日 By Simon
    pip3.7 install gitpython
==================================================================
'''

from datetime import datetime
import os
import uuid
import csv
import git
from git import RemoteProgress
from multiprocessing import Process, Manager, Lock, RLock
from src.libs.log import L

def TM(): return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')



class CloneProgress(RemoteProgress):
    def __init__(self, jobs, _id):
        git.RemoteProgress.__init__(self)
        self.jobs = jobs
        self.id = _id
        
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            self.jobs[self.id]["progress"] = "%s,%s" % (message, 100.0 * cur_count / max_count)
        '''End If'''

class CloneJob(Process):
    def __init__(self, G, url, _id):
        super().__init__()
        self.id = _id
        self.url = url
        self.status = 0
        self.folder = str(uuid.uuid1())
        job = G.mg.dict()
        job['url'], job['status'], job['times'], job['progress'] = url, 0, 1, ""
        job['id'], job['folder'], job['completeTime'] = _id, self.folder, None
        G.jobs[self.id] =job
        self.jobs = G.jobs
        
    def run(self):
        self.jobs[self.id]['status'] = 1
        dst = './repo/' + self.folder
        if not os.path.exists(dst): os.mkdir(dst)
        for i in range(3):
            if i > 0: L.info("The %sth time Request: %s now" % (i + 1, self.url))
            self.status = self.clone(dst)
            if self.status == 2: break
        '''End For'''
        self.jobs[self.id]['status'] = self.status
        self.write_result()
        
    def clone(self, dst):
        try:
            git.Repo.clone_from(self.url, dst, progress=CloneProgress(self.jobs, self.id))
            return 2
        except Exception as e:
            self.jobs[self.id]['times'] += 1
            return -1
        '''End Try'''
    
    def write_result(self):
        L.info("Job %s run End with status %s." % (self.id, self.status))
        completeTime = TM()
        self.jobs[self.id]['completeTime'] = completeTime
        
        with open("./result.csv", "a") as f:
            line = '%s,%s,%s,%s,%s\n' % (self.id, self.status, self.folder, self.url, completeTime)
            f.write(line)
        '''End With'''
    
    @staticmethod    
    def load_history(G):
        idx = 0
        with open("./result.csv", "r") as f:
            for d in csv.reader(f, skipinitialspace=True):
                _id, status, folder = int(d[0]), int(d[1]), d[2]
                url, tm = d[3], d[4]
                info = G.mg.dict()
                info['id'], info['status'], info['folder'] = _id, status, folder
                info['url'], info['progress'], info['completeTime'] = url, None, tm
                if _id > idx: idx = _id
                G.jobs[_id] = info
        '''End With'''
        G.idx = idx + 1
'''========================================End Class===================================================='''


def clone_res(G, url, name):
    pass
    '''============================TODO：wget文件，获取进度==============================='''
    
    return start_job(G, url)
    
    
def start_job(G, url):
    _id = G.get_id()
    cj = CloneJob(G, url, _id)
    cj.start()
    return _id

    

if __name__ == '__main__':
    start_job()
    
    pass