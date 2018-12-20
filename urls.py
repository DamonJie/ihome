from handlers.VerifyCode import PicCodeHandler,SMSCodeHandler
from handlers.BaseHandler import StaticFileBaseHandler
from handlers.Passport import RegisterHandler,CheckLoginHandler,LoginHandler,LogoutHandler
from handlers.House import IndexHandler,AreaInfoHandler,HouseInfoHandler,HouseImageHandler,MyHouseHandler,HouseListHandler,HouseListRedisHandler
from handlers.Profile import ProfileHandler,NameHandler,AvatarHandler,AuthHandler
from handlers.Orders import OrderHandler,MyOrdersHandler,AcceptOrderHandler,RejectOrderHandler,OrderCommentHandler
import os

urls=[
    (r"/api/profile/auth", AuthHandler),
    (r"/api/profile/name", NameHandler), # 个人主页修改用户名
    (r"/api/profile/avatar",AvatarHandler), # 用户上传头像
    (r"/api/profile", ProfileHandler),
    (r"/api/login", LoginHandler),
    (r"/api/logout", LogoutHandler),
    (r'^/api/house/my$', MyHouseHandler), # 查询用户发布的房源
    (r'^/api/house/image$', HouseImageHandler), # 上传房屋图片
    (r'^/api/house/info$', HouseInfoHandler), # 上传房屋的基本信息
    (r"/api/house/area", AreaInfoHandler),
    (r'^/api/house/index$', IndexHandler),
    (r'^/api/house/list2$', HouseListRedisHandler), # 房屋过滤列表数据
    (r'^/api/house/list$', HouseListHandler), # 房屋过滤列表数据
    (r"/api/check_login",CheckLoginHandler),
    (r"/api/register",RegisterHandler),
    (r"/api/piccode",PicCodeHandler),
    (r"/api/smscode",SMSCodeHandler),
    (r'^/api/order$', OrderHandler), # 下单
    (r'^/api/order/my$', MyOrdersHandler), # 我的订单，作为房客和房东同时适用
    (r'^/api/order/accept$', AcceptOrderHandler), # 接单
    (r'^/api/order/reject$', RejectOrderHandler), # 拒单
    (r'^/api/order/comment$', OrderCommentHandler),
    (r'/(.*)',StaticFileBaseHandler,dict(path=os.path.join(os.path.dirname(__file__),"templates"),default_filename="index.html")),
]