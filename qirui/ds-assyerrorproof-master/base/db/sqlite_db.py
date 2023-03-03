#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   key_value_db.py

    Key-Value 数据库抽象接口接口

参考资料:
    https://stackoverflow.com/questions/47233562/key-value-store-in-python-for-possibly-100-gb-of-data-without-client-server
    shelve, sqlite3 (sqlitedict provides key-value interface to SQLite database.), lmdb / LevelDB / RocksDB / bsddb, wiredtiger
"""

from abc import  abstractmethod
class KeyValueDB():
    """
        键值对数据库的抽象接口
    """
    @abstractmethod
    def count(self, **kwargs):
        """ 返回记录数 """
        raise NotImplementedError

    @abstractmethod
    def get(self, key, default=None, **kwargs):
        """ 获取值"""
        raise NotImplementedError

    @abstractmethod
    def put(self, key, value, **kwargs):
        """ 设置值 """
        raise NotImplementedError

    def append(self, key, value, **kwargs):
        """ 追加值 """
        raise NotImplementedError

    def exist(self, key):
        return self.get(key) is not None

    def items(self, offset=0, count=-1):
        """ 遍历指定范围记录的迭代器, 默认是所有记录 """
        raise NotImplementedError


from sqlitedict import SqliteDict

class SqliteDictKVDB(KeyValueDB):
    def __init__(self, dbfile="siftdb1.sqlite"):
        self.dbfile = dbfile
        self.mydict = SqliteDict(dbfile, autocommit=True)

    def __del__(self):
        # SqliteDict 对象销毁时会自动关闭，不需要显式调用 close(), 两次调用程序会卡在 close 上
        pass

    def count(self, **kwargs):
        return len(self.mydict)

    def get(self, key, default=None, **kwargs):
        return self.mydict.get(key, default)

    def put(self, key, value, **kwargs):
        self.mydict[key] = value

    def append(self, key, value, **kwargs):
        self.mydict[key] = self.mydict.get(key, []) + [value]

    def items(self, offset=0, count=-1):
        return self.mydict.items()

    def delete(self, key, **kwargs):
        return self.mydict.pop(key, None)

        # TypeError: 'generator' object is not subscriptable
        # if count < 0:
        #     return self.mydict.items()[offset:]
        # else:
        #     return self.mydict.items()[offset:(offset+count)]

