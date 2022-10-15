from hashlib import md5
import json
from os import path
import os
import subprocess
from uuid import uuid4
from tinydb import TinyDB, Query
from dataclass.GlobalConfig import GlobalConfig

CONFIG_FILE = "./config.json"
config = GlobalConfig('', 16)


def initBasicEnv():
    global config
    if not path.exists(CONFIG_FILE):
        print("第一次使用，请输入要保存数据库的地方: ")
        basicPath = ''
        inPath = input()
        print(f'你设置了数据库保存路径为: {inPath}, 正在初始化...')
        basicPath = inPath
        with open(CONFIG_FILE, 'w+', encoding='utf-8') as config:
            config.write(json.dumps({
                'basePath': basicPath,
                'thread': 16
            }, ensure_ascii=False))
            config.flush()
            config.close()
    with open(CONFIG_FILE, 'r', encoding='utf-8') as cfg:
        jsons = cfg.read()
        js = json.loads(jsons)
        config.basePath = js['basePath']
        config.executeThread = int(js['thread'])
    print("Initialization: 基本数据环境初始化完成。")
    config.db = TinyDB(f'{config.basePath}/tingDB.json')
    config.executeUrl = f'{config.basePath}/dmg'

    # parse all files
    lis = ScanApps(config.executeUrl)
    for a in lis:
        (file, ext) = path.splitext(a)
        if ext == '.dmg':
            getDmgInfo(a.replace(" ", "\ "))


def getDmgInfo(files):
    print(files)
    lhash = md5(files.encode('utf-8')).hexdigest().upper()
    lhash = '/Volumes/TMP_'+lhash
    hdiutil_process = f'hdiutil attach {files} -mountpoint {lhash} -plist'
    p = subprocess.Popen(hdiutil_process,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    
    (plist, err) = p.communicate()
    if err:
        print("%s" % (err.decode('utf-8')))

    if p.returncode == 0:
        readAppInfo(lhash)
        detachDmg(lhash)
        return True
    else:
        return False


def readAppInfo(lhash):
    lis = ScanApps(lhash, True)
    print(lis)


def detachDmg(devName):
    devComm = f'hdiutil detach {devName}'
    p = subprocess.Popen(devComm, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    (plist, err) = p.communicate()
    if err:
        print("%s" % (err.decode('utf-8')))
    if p.returncode == 0:
        return True
    else:
        return False


def ScanApps(paths: str, searchTop=False):
    """枚举目录下所有文件

    Args:
        paths (str): 路径地址 要扫描的文件夹目录 不需要带/符号结尾 如C:/dmgs

    Returns:
        list[str]: 返回文件列表
    """
    global config
    lis_ret = []
    for a in os.listdir(paths):
        mfile = paths+"/"+a
        if path.isdir(mfile) and not searchTop:
            lis = ScanApps(mfile)
            lis_ret.extend(lis)
        else:
            lis_ret.append(mfile)
    return lis_ret


if __name__ == '__main__':
    initBasicEnv()
