from flask import Flask, request, abort
import hashlib
from bs4 import BeautifulSoup
import aiml
import os

# AIML
alice = aiml.Kernel()
os.chdir('./alice')
alice.learn("startup.xml")
alice.respond('LOAD ALICE')

# 微信的token令牌
WECHAT_TOKEN = "haohao"

app = Flask(__name__)


@app.route('/wechat', methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        """对接微信公众号服务器"""
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")

        # 校验参数
        if not all([signature, timestamp, nonce]):
            abort(400)

        # 按照微信的流程进行计算签名
        array = [WECHAT_TOKEN, timestamp, nonce]
        # 排序
        array.sort()
        # 拼接字符串
        tmp_str = "".join(array)
        # 进行sha1加密，得到正确的签名值
        sign = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()
        print(sign == signature)
        # 将自己计算的签名值与请求的签名参数进行对比
        if signature != sign:
            abort(403)
        else:
            return echostr
    else:
        xml_in = request.get_data().decode()
        soup = BeautifulSoup(xml_in, "html.parser")
        toUser = soup.find("fromusername").text
        fromUser = soup.find("tousername").text
        time = soup.find("createtime").text
        text = alice.respond(soup.find("content").text)
        reply = "<xml><ToUserName><![CDATA[" + toUser + "]]></ToUserName><FromUserName><![CDATA[" + fromUser + "]]></FromUserName><CreateTime>" + time + "</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[" + text + "]]></Content></xml>"
        return reply


if __name__ == '__main__':
    app.run(port=8000, debug=False)
