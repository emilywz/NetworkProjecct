"""
数据库操作,提供数据服务端需要的数据
"""

import pymysql,hashlib

SALT="#%%&#@"

# 密码加密
def hash_sha512(password):
    hash_obj=hashlib.sha512(SALT.encode())
    hash_obj.update(password.encode())
    return hash_obj.hexdigest()


class DictDataBaseModel:
    def __init__(self,host="localhost",
                port=3306,
                user='root',
                password='123456',
                database=None,
                charset='utf8'):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database
        self.charset=charset
        self.connect_db()

    def connect_db(self):
        # 连接数据库
        self.db = pymysql.connect(host=self.host,
                              port=self.port,
                              user=self.user,
                              password=self.password,
                              database=self.database,
                              charset=self.charset)

    def create_cur(self):
        # 生成游标对象(操作数据库,执行sql语句)
        self.cur = self.db.cursor()

    def close(self):
        # 关闭游标和数据库连接
        self.cur.close()
        self.db.close()

    def handle_register_data(self,name,password):
        sql_pwd=hash_sha512(password)

        try:
            sql = "insert into user(name,password) values(%s,%s)"
            self.cur.execute(sql, [name, sql_pwd])
            self.db.commit()
        except Exception:
            self.db.rollback()
        else:
            return True


    def handle_login_data(self, name, password):

        sql_pwd = hash_sha512(password)

        sql = "select name from user where name=%s and password=%s;"
        self.cur.execute(sql, [name, sql_pwd])
        data = self.cur.fetchone()

        if data:
            return True
        else:
            return False

    def handle_query_dict(self,word):
        sql="select mean from words where word=%s"
        self.cur.execute(sql,[word])
        data=self.cur.fetchone()
        if data:
            return data[0]



    def add_history_word(self,name,word):
        try:
            sql="insert into history(name,word_info) values (%s,%s);"
            self.cur.execute(sql, [name,word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def handle_check_history(self,name):
        sql="select name,word_info,notetime from history where name=%s order by notetime desc limit 10;"
        self.cur.execute(sql,[name])
        data=self.cur.fetchall()
        if data:
            return data

if __name__ == '__main__':
    db=DictDataBaseModel()
    db.add_history_word("Abby","a")






