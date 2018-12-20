import logging
import constants

from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
from utils.qiniu_storage import storage
from utils.commons import required_login

class ProfileHandler(BaseHandler):
    """个人信息"""
    @required_login
    def get(self):
        user_id = self.session.data['user_id']
        try:
            ret = self.db.get_one("select up_name,up_mobile,up_avatar from ih_user_profile where up_user_id=%s", user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errcode":RET.DBERR, "errmsg":"get data error"})
        if ret[2]:
            img_url = constants.QINIU_URL_PREFIX + ret[2]
        else:
            img_url = None
        self.write({"errcode":RET.OK, "errmsg":"OK",
                    "data":{"user_id":user_id, "name":ret[0], "mobile":ret[1], "avatar":img_url}})

class NameHandler(BaseHandler):

    @required_login
    def post(self):
        user_id=self.session.data["user_id"]
        name=self.json_args.get("name")
        if name in (None,""):
            return self.write({"errcode":RET.PARAMERR,"errmsg":"params error"})
        try:
            self.db.update("update ih_user_profile set up_name=%s where up_user_id=%s",(name,user_id))
        except Exception as e:
            logging.error(e)
            return self.write({"errcode":RET.DBERR,"errmsg":"name has exist"})

        self.session.data["name"]=name
        try:
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write({"errcode":RET.OK,"errmsg":"OK"})

class AvatarHandler(BaseHandler):

    @required_login
    def post(self):
        files=self.request.files.get("avatar")
        if not files:
            return self.write(dict(errcode=RET.PARAMERR,errmsg="未传图片"))
        avatar=files[0]["body"]
        try:
            file_name=storage(avatar)
        except Exception as e:
            logging.error(e)
            return self.write(dict(error=RET.THIRDERR,errmsg="上传失败"))
        # 从session数据中取出user_id
        user_id = self.session.data["user_id"]
        # 保存图片名（即图片url）到数据中
        sql = "update ih_user_profile set up_avatar=%s where up_user_id=%s"
        try:
            row_count = self.db.update(sql, (file_name,user_id))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="保存错误"))
        self.write(dict(errcode=RET.OK, errmsg="保存成功", data="%s%s" % (constants.QINIU_URL_PREFIX, file_name)))

class AuthHandler(BaseHandler):

    @required_login
    def get(self):
        user_id=self.session.data["user_id"]

        try:
            ret=self.db.get_one("select up_real_name,up_id_card from ih_user_profile where up_user_id=%s",(user_id,))
        except Exception as e:
            logging.error(e)
            return self.write({"errcode":RET.DBERR,"errmsg":"get data failed"})
        logging.debug(ret)
        if not ret:
            return self.write({"errrcode":RET.NODATA,"errmsg":"no data"})
        self.write({"errcode":RET.OK,"errmsg":"OK","data":{"real_name":ret[0],"id_card":ret[1]}})

    @required_login
    def post(self):
        user_id = self.session.data["user_id"]
        real_name = self.json_args.get("real_name")
        id_card = self.json_args.get("id_card")
        if real_name in (None, "") or id_card in (None, ""):
            return self.write({"errcode": RET.PARAMERR, "errmsg": "params error"})
        # 判断身份证号格式
        try:
            self.db.update("update ih_user_profile set up_real_name=%s,up_id_card=%s where up_user_id=%s",(real_name, id_card, user_id))
        except Exception as e:
            logging.error(e)
            return self.write({"errcode": RET.DBERR, "errmsg": "update failed"})
        self.write({"errcode": RET.OK, "errmsg": "OK"})