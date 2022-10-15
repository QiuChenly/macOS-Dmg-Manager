

from dataclasses import dataclass
import json
from os import path
import os
from tinydb import TinyDB, Query

CONFIG_FILE = "./config.json"


@dataclass
class GlobalConfig:
    basePath: str
    """
    相对路径的基本点
    """
    executeThread: int
    """
    并行任务
    """
    db: TinyDB
    """
    数据库文件地址
    """
    executeUrl: str
    """
    可执行文件全路径
    """

    def __init__(self,  basePath: str, threadSize: int) -> None:
        self.basePath = basePath
        self.executeThread = threadSize


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


if __name__ == '__main__':
    initBasicEnv()
