#!/usr/bin/env python
# encoding: utf-8

from threading import Thread
from collections import namedtuple
import time

from wxbot import WXBot

MessageInfo = namedtuple("MessageInfo", [
    "user", "name", "remark", "sex", "province", "city",
])

conf = {
    "response": {
        u"中秋快乐": u"同乐同乐",
    },
    "message": "{info.remark}，中秋快乐！"
}


class GreetingBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)
        self.wx_thread = Thread(target=self.run)
        self.wx_thread.setDaemon(True)

    def handle_msg_all(self, msg):
        if msg.get("msg_type_id") != 4:  # friends message only
            return
        content = msg.get("content")
        if not content or content.get("type"):  # text message only
            return
        content_data = content.get("data")
        for k, i in conf["response"].items():
            if k in content_data:
                self.send_msg_by_uid(i, msg['user']['id'])

    def run_background(self):
        self.wx_thread.start()

    def greet(self, message_info):
        message = conf["message"].format(info=message_info)
        try:
            for i in range(3):
                if self.send_msg(message_info.name, message):
                    break
        except Exception as err:
            print err


def get_friend_message(index, contact):
    print "NickName:", contact.get("NickName")
    print "Sex:", "Man" if contact.get("Sex") == 1 else "Female"
    print "RemarkName:", contact.get("RemarkName")
    print "Province:", contact.get("Province")
    print "City:", contact.get("City")

    remark = raw_input("%s enter remark:" % index)
    if not remark:
        return
    if remark.isspace():
        remark = contact.get("RemarkName") or contact.get("NickName")
    return MessageInfo(
        user=contact.get("UserName"), name=contact.get("NickName"),
        remark=remark, sex="Man" if contact.get("Sex") == 1 else "Female",
        province=contact.get("Province"), city=contact.get("City"),
    )


def main():
    bot = GreetingBot()
    bot.run_background()
    time.sleep(10)
    index = int(raw_input("login and press enter to continue") or 0)

    for i, e in enumerate(bot.contact_list):
        if i <= index:
            continue

        message_info = get_friend_message(i, e)
        if not message_info:
            continue
        bot.greet(message_info)

if __name__ == "__main__":
    main()
