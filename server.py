from tornado.options import define,options
from mymysql import PackSqlOpt
from urls import urls
from tornado.ioloop import IOLoop
import tornado.web
import config
import tornado.options
import tornado.httpserver
import redis

define("port",default=9006,type=int,help="run server on the given port")

class Application(tornado.web.Application):
    def __init__(self,*args,**kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db=PackSqlOpt(**config.mysql)
        self.redis=redis.StrictRedis(**config.redis)

if __name__ == '__main__':
    options.log_file_prefix=config.log_path
    options.logging=config.log_level
    tornado.options.parse_command_line()
    app=Application(
        urls,
        **config.settings
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port,address="192.168.0.110")
    IOLoop.current().start()