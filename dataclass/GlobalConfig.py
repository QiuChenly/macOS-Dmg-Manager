from dataclasses import dataclass

from tinydb import TinyDB


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
