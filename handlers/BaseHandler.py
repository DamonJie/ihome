import json

from tornado.web import RequestHandler,StaticFileHandler
from utils.session import Session


class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        if self.request.headers.get("Content-Type","").startswith("application/json"):
            try:
                self.json_args = json.loads(str(self.request.body,encoding='utf-8'))
            except:
                self.json_args=None
        else:
            self.json_args = None

    def set_default_headers(self):
        """设置默认json格式"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def get_current_user(self):
        """判断用户是否登录"""
        self.session = Session(self)
        return self.session.data

class StaticFileBaseHandler(StaticFileHandler):

    def __init__(self,*args,**kwargs):
        super(StaticFileBaseHandler, self).__init__(*args,**kwargs)
        self.xsrf_token