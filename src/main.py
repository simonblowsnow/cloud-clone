#coding: utf8
'''
==================================================================
Created on 2021年12月13日 By Simon

==================================================================
'''

import ctypes
from multiprocessing import Manager, freeze_support
from src.clone import clone_res, CloneJob # load_history
from src.libs.conf import GlobalData as G
from flask import Flask, request

app = Flask(__name__)


'''
原理：
    1.接收下载请求
    2.返回资源ID
    3.下载资源，3次重试
    4.记录状态，写入result.csv
    5.接受状态查询

status: 0 - 未执行，1 - 执行中，2 - 已完成，3 - 已失败
'''

@app.route('/')
def index():
    return 'Hello World'

@app.route('/cloneRes')
def _clone_res():
    url = request.form.get('url', None)
    name = request.form.get('name', None)
    # if not url: return {"error": 1, "message": "参数错误，缺少url"}
    
    url1 = "https://github.com/dolanmiu/docx.git"
    url2 = "https://github.com/rishit-singh/OpenShell.git"
    url3 = "https://github.com/microsoft/monaco-editor.git"
    url = url2
    
    _id = clone_res(G, url, name)
    return {"error": 0, "data": {"jobId": _id}}


@app.route('/requestStatus')
def request_status():
    _id = int(request.args.get('jobId', "-1"))
    if _id not in G.jobs: return {"error": 1, "message": "网络错误，请重试！"}
    j = G.jobs[_id]
    return {"error": 0, "data": {"status": j["status"], "folder": j["folder"], 
                "url": j["url"], "progress": j["progress"]}}
    


if __name__ == '__main__':
    freeze_support()
    mg = Manager()
    G.mg, G.idx, G.jobs = mg, mg.Value(ctypes.c_int, 0), mg.dict()
    CloneJob.load_history(G)
    app.run(host = "0.0.0.0", port = 8885)
    
    