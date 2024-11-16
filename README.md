<div align="center">


_✨ 基于 [机器人开放平台API](https://bot.q.qq.com/wiki/develop/api/)和[GLM-4 模型](https://open.bigmodel.cn/) 进行开发的QQbot葡叶酱 ✨_


</div>

## 准备工作

葡叶酱bot兼容的Python最低版本是Python3.8。
低于Python3.8会运行失败。


### 使用

需要使用的地方`import botpy`(因为文件中有botpy软件包，可以选择不下载)


```python
import botpy
```


## 使用方式

1. 配置文件
修改配置文件 `config.yaml`，配置好自己的机器人信息。
添加自己的GLM-4的API Key在运行文件的else中，以保证在没有固定回答时调用GLM-4 API。
2. 运行文件
双击 `run.bat` 或者直接运行 `main.py`



## 文件地址

[`handlers`](./handlers/) 目录下存放要运行的代码文件 

    handlers/
    .
    ├── README.md
    ├── resources                    # 资源文件
    │   ├── images
    │   │   ├── drawing              # 抽签用图片文件
    │   │   │   ├── 月宫亚由中吉87.png
    │   │   │   ├── ……
    ├── channel_files_handlers.py    # 频道文件相关事件
    ├── channel_handlers.py          # 频道消息相关事件
    ├── group_handlers.py            # 群消息相关事件
    ├── group_files_handlers.py      # 群文件相关事件(因为去重问题，可能会发送失败）
    ├── private_handlers.py          # 私信相关事件
    


## 环境配置（直接运行可跳过，如果二次开发，可以配置一下）

```bash
pip install -r requirements.txt   # 安装依赖的pip包

pre-commit install                 # 安装格式化代码的钩子
```
