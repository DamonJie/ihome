import pymysql

# def singleton(cls,*args,**kwargs):
#     instances={}
#     def _singlenton():
#         if cls not in instances:
#             instances[cls]=cls(*args,**kwargs)
#         return instances[cls]
#     return _singlenton()
#
# @singleton
class PackSqlOpt:
    def __init__(self, host, username, password, dbname):
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname

    def connect(self):
        #连接数据库并创建一个cursor游标对象
        self.conn = pymysql.connect(self.host, self.username, self.password, self.dbname)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self,sql,params=()):
        #获取单行数据
        data=None
        try:
            self.connect()
            self.cursor.execute(sql,params)
            #执行查询语句时，获取查询结果集的第一个行数据，返回一个元组
            data=self.cursor.fetchone()
            self.close()
        except Exception as e:
            print("查询数据失败",e)
        return data

    def get_all(self,sql,params=()):
        #获取全部数据
        data=()
        try:
            self.connect()
            self.cursor.execute(sql,params)
            #执行查询时，获取结果集的所有行，一行构成一个元组，再将这些元组装入一个元组返回
            data=self.cursor.fetchall()
            self.close()
        except Exception as e:
            print("查询数据失败",e)
        return data

    def insert(self,sql,params=()):
        return self.__edit(sql,params)

    def update(self,sql,params=()):
        return self.__edit(sql,params)

    def delete(self,sql,params=()):
        return self.__edit(sql,params)

    def __edit(self,sql,params):
        #通过insert，updata,delete方法的调用，进行数据的操作
        count=0
        try:
            self.connect()
            count=self.cursor.execute(sql,params)#count返回影响行数
            #commit()方法提交事务，对数据库进行的操作提交后才会生效
            self.conn.commit()
            self.close()
        except Exception as e:
            print("更新事务失败",e)
            #rollback()方法放弃之前的操作
            self.conn.rollback()
        return count