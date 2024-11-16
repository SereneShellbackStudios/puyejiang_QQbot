import asyncio
import os
import botpy
from botpy.ext.cog_yaml import read
import importlib
from botpy import logging

_log = logging.get_logger()

# 读取配置文件
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

# 模块加载配置
MODULES = [
    {"module": "handlers.channel_handler", "intents": botpy.Intents(public_guild_messages=True)},
    {"module": "handlers.channel_files_handler", "intents": botpy.Intents(public_guild_messages=True)},
    {"module": "handlers.group_handler", "intents": botpy.Intents(public_messages=True)},
    {"module": "handlers.group_files_handler", "intents": botpy.Intents(public_messages=True)},
    {"module": "handlers.private_handler", "intents": botpy.Intents(direct_message=True, public_guild_messages=True)},
]

class MultiClientManager:
    def __init__(self, config, modules):
        self.config = config
        self.modules = modules
        self.clients = []

    async def start_clients(self):
        tasks = []
        for module_info in self.modules:
            module_name = module_info["module"]
            intents = module_info["intents"]

            # 动态导入模块
            module = importlib.import_module(module_name)
            MyClient = getattr(module, "MyClient")

            # 初始化客户端
            client = MyClient(intents=intents, is_sandbox=True)
            self.clients.append(client)

            # 启动客户端
            tasks.append(client.start(appid=self.config["appid"], secret=self.config["secret"]))

        # 并行运行所有客户端
        await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.start_clients())


if __name__ == "__main__":
    manager = MultiClientManager(test_config, MODULES)
    manager.run()
