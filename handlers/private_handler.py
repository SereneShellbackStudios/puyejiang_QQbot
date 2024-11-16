import botpy
from botpy import logging
from botpy.message import Message
import os
import asyncio
import botpy
from botpy import logging

from botpy.message import DirectMessage, Message
from botpy.ext.cog_yaml import read
from zhipuai import ZhipuAI

_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"私信机器人 「{self.robot.name}」 已启动！")

    async def on_at_message_create(self, message: Message):
        # 根据频道内容判断是否应该进行私信回复
        if "/私信" in message.content:
            dms_payload = await self.api.create_dms(message.guild_id, message.author.id)
            _log.info("发送私信")
            await self.api.post_dms(dms_payload["guild_id"], content="hello", msg_id=message.id)

    async def on_direct_message_create(self, message: DirectMessage):
        # 获取私信内容
        private_message_content = message.content
        _log.info(f"收到私信: {private_message_content}")

        # 检查私信内容是否包含特定关键词
        if "你好" in private_message_content:
            response = "你好！很高兴见到你。"
        elif "帮助" in private_message_content:
            response = "我可以帮助你解决各种问题，请告诉我你需要什么帮助。"
        elif "吃掉" in private_message_content:
            response = "救命啊！有人要吃小葡叶了！"
        else:

            # 使用 GLM-4 模型生成回答

            input_text = message.content
            client = ZhipuAI(api_key="xxxxxxxxxxxxxxxxxxxxxxxx")  # 请填写您自己的APIKey
            response = client.chat.asyncCompletions.create(
                model="glm-4",  # 请填写您要调用的模型名称
                messages=[
                    {
                        "role": "user",
                        "content": input_text
                    }
                ],
            )

            task_id = response.id
            task_status = ''
            get_cnt = 0
            while task_status != 'SUCCESS' and task_status != 'FAILED' and get_cnt <= 40:
                result_response = client.chat.asyncCompletions.retrieve_completion_result(id=task_id)
                task_status = result_response.task_status
                if task_status == 'SUCCESS':
                    reply_content = result_response.choices[0].message.content
                    await message.reply(content=reply_content)
                elif task_status == 'FAILED':
                    await message.reply(content="对不起，生成回答时发生错误。")
                else:
                    await asyncio.sleep(2)
                    get_cnt += 1

        # 回复私信
        await self.api.post_dms(
            guild_id=message.guild_id,
            content=response,
            msg_id=message.id,
        )
