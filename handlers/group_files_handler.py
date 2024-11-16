# -*- coding: utf-8 -*-

import os
import random
import uuid

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

# 定义图片URL列表
image_urls = [
    "https://s2.loli.net/2024/11/04/NELeguoc8YmHK9z.png",
    "https://s2.loli.net/2024/11/04/dZzgP1tq8o2WVGX.png",
    "https://s2.loli.net/2024/11/05/63zFAKl25vuDTbV.png"
    "https://s2.loli.net/2024/11/05/1ub4kxKqihF5mVC.png"
    "https://s2.loli.net/2024/11/04/IXf5ENR82v3UpKy.png",
    "https://s2.loli.net/2024/11/04/KFhICNk6wDeA4jU.png",
    "https://s2.loli.net/2024/11/04/avVFAk93DyrKsNu.png",
    "https://s2.loli.net/2024/11/04/NJ7twikVr4FfUhM.png",
    "https://s2.loli.net/2024/11/04/YgGZIQ9tORpm6wr.png",
    "https://s2.loli.net/2024/11/04/FYGmRjexuM48WKf.png",

    # 更多图片URL...
]

# 定义运势列表
fortunes = [
    "大吉", "中吉", "小吉", "吉", "平", "末吉", "凶", "大凶"
]

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"群聊文件机器人 「{self.robot.name}」 已启动！")


    async def on_group_at_message_create(self, message: GroupMessage):
        if "抽签" in message.content:
            fortune = random.choice(fortunes)
            image_url = random.choice(image_urls)

            unique_id = str(uuid.uuid4())

            await message.reply(content=f"恭喜您抽签成功，您今天的运势是：{fortune} (标识符: {unique_id})")

            uploadMedia = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,
                url=image_url
            )

            await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,
                media=uploadMedia
            )