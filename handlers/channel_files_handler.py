import datetime
import random

import os

from datetime import datetime

import botpy
from botpy import logging

from botpy.message import Message


_log = logging.get_logger()

# 图片资源路径
IMAGE_DIR = "handlers/resource/images/drawing"
# 用户抽签记录
user_sign_records = {}

# 读取图片资源
def load_images():
    images = []
    for filename in os.listdir(IMAGE_DIR):
        if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
            images.append(os.path.join(IMAGE_DIR, filename))
    return images

images = load_images()



class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"频道文件机器人 「{self.robot.name}」 已启动！")


    async def on_at_message_create(self, message: Message):
        content = message.content.strip().lower()
        user_id = message.author.id
        today = datetime.now().date()

        if user_id not in user_sign_records:
            user_sign_records[user_id] = {}

        user_record = user_sign_records[user_id]

        if "抽签" in content:
            if today not in user_record:
                # 随机选择一张图片
                selected_image = random.choice(images)
                user_record[today] = selected_image
            else:
                selected_image = user_record[today]

            await message.reply(content="抽签成功，您今天的运势是：")
            await message.reply(file_image=selected_image)