import os

BASE_DIRS=os.path.dirname(__file__)


#数据库配置
mysql={
    "host":"192.168.0.110",
    "username":"root",
    "password":"123456",
    "dbname":"ihome"
}

redis={
    "host":"127.0.0.1",
    "port":6379
}

#配置
settings=dict(
        # autoescape=None,
        static_path=os.path.join(BASE_DIRS, "static"),
        template_path=os.path.join(BASE_DIRS, "templates"),
        cookie_secret="FhLXI+BRRomtuaG47hoXEg3JCdi0BUi8vrpWmoxaoyI=",
        debug=True,
        xsrf_cookies=True,
    )

log_path=os.path.join(os.path.dirname(__file__),"logs/log")
log_level="debug"

# 密码加密密钥
passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="