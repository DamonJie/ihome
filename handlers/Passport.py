from handlers.BaseHandler import BaseHandler
from tornado.web import RequestHandler
from utils.response_code import RET
from utils.session import Session
from utils.commons import required_login
import logging
import hashlib
import config
import re

class RegisterHandler(BaseHandler):
    def post(self):
        mobile=self.json_args.get("mobile")
        sms_code=self.json_args.get("phonecode")
        password=self.json_args.get("password")

        if not all([mobile,sms_code,password]):
            return self.write(dict(errcode=RET.PARAMERR,errmsg="参数不完整"))
        if not re.match(r"^1\d{10}$",mobile):
            return self.write(dict(errcode=RET.DATAERR,errmsg="手机号格式错误"))

        if "2468"!=sms_code:
            try:
                real_sms_code=self.redis.get("sms_code_%s"%mobile)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR,errmsg="查询验证码出错"))

            if not real_sms_code:
                print(real_sms_code)
                return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))

            if str(real_sms_code,encoding="utf-8") != sms_code:
                print(str(real_sms_code,encoding="utf-8"))
                print(sms_code)
                return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误"))

            try:
                self.redis.delete("sms_code_%s" % mobile)
            except Exception as e:
                logging.error(e)

        print(password)
        print(type(password))
        print(config.passwd_hash_key)
        passwd = hashlib.sha256(bytes(password + config.passwd_hash_key,encoding="utf-8")).hexdigest()
        sql = "insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%s, %s, %s);"
        try:
            user_id = self.db.insert(sql,(mobile, mobile, passwd))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAEXIST, errmsg="手机号已存在"))

        # 用session记录用户的登录状态
        session = Session(self)
        session.data["user_id"] = user_id
        session.data["mobile"] = mobile
        session.data["name"] = mobile
        try:
            session.save()
        except Exception as e:
            logging.error(e)

        self.write(dict(errcode=RET.OK, errmsg="注册成功"))

class CheckLoginHandler(BaseHandler):
    """检查登陆状态"""
    def get(self):
        # get_current_user方法在基类中已实现，它的返回值是session.data（用户保存在redis中
        # 的session数据），如果为{} ，意味着用户未登录;否则，代表用户已登录
        if self.get_current_user():
            self.write({"errcode":RET.OK, "errmsg":"true", "data":{"name":self.session.data.get("name")}})
        else:
            self.write({"errcode":RET.SESSIONERR, "errmsg":"false"})

class LoginHandler(BaseHandler):
    """登录"""
    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")

        # 检查参数
        if not all([mobile, password]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))
        if not re.match(r"^1\d{10}$", mobile):
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号错误"))

        # 检查秘密是否正确
        res = self.db.get_one("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%s"%mobile)
        password = hashlib.sha256(bytes(password + config.passwd_hash_key,encoding="utf-8")).hexdigest()
        if res and res[2] == password:
            # 生成session数据
            # 返回客户端
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res[0]
                self.session.data['name'] = res[1]
                self.session.data['mobile'] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write(dict(errcode=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errcode=RET.DATAERR, errmsg="手机号或密码错误！"))


class LogoutHandler(BaseHandler):
    """退出登录"""
    @required_login
    def get(self):
        # 清除session数据
        # sesssion = Session(self)
        self.session.clear()
        self.write(dict(errcode=RET.OK, errmsg="退出成功"))