import botpy
from botpy import logging
from botpy.message import Message
import asyncio
import os
import re
from datetime import datetime
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
from zhipuai import ZhipuAI

_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"群聊机器人 「{self.robot.name}」 已启动！")

    async def on_group_at_message_create(self, message: GroupMessage):
        _log.info(f"Received message: {message.content}")

        # 生日提醒功能
        if re.search(r'\b生日提醒\b', message.content):
            today = datetime.now().strftime('%m-%d')
            birthdays = {
                "01-03": ["雾岛 聖（《AIR》）"],
                "01-05": ["桐生 美也（《Heaven Burns Red》）"],
                "01-06": ["泽渡 真琴（《Kanon》）", "白河 ユイナ（《Heaven Burns Red》）"],
                "01-07": ["月宫 あゆ（《Kanon》）"],
                "01-12": ["直枝架夜（《Kud Wafter》）"],
                "01-15": ["水濑 いちご（《Heaven Burns Red》）"],
                "01-17": ["直枝 理树（《Little Busters》）"],
                "01-18": ["伊吹 公子（《CLANNAD》）"],
                "01-23": ["LUNAR-Q（《LUNARiA》）"],
                "01-26": ["ヴリティカ・ バラクリシュナン（《Heaven Burns Red》）"],
                "01-29": ["川澄 舞（《Kanon》）"],
                "02-01": ["美坂 栞（《Kanon》）,岡崎 汐（《CLANNAD》）"],
                "02-02": ["野村 美希（《Summer Pockets》）"],
                "02-07": ["佐月 マリ（《Heaven Burns Red》）"],
                "02-09": ["三谷 良一（《Summer Pockets》）"],
                "02-14": ["东城 つかさ（《Heaven Burns Red》）"],
                "02-17": ["千里 朱音（《Rewrite》）,春原 陽平（《CLANNAD》）"],
                "02-22": ["神崎 アーデルハイド（《Heaven Burns Red》）"],
                "02-24": ["町村 玲央奈（《LOOPERS》）"],
                "02-26": ["マリア・デ・ アンジェリス（《Heaven Burns Red》）"],
                "03-01": ["美坂 香里（《Kanon》）"],
                "03-04": ["命 吹雪（《Heaven Burns Red》）"],
                "03-05": ["西門 貴明（《LOOPERS》）"],
                "03-06": ["井上 晶（《Rewrite》）"],
                "03-13": ["来ヶ谷 唯湖（《Little Busters!》）"],
                "03-18": ["柊木 梢（《Heaven Burns Red》）"],
                "03-21": ["小笠原 緋雨（《Heaven Burns Red》）"],
                "03-25": ["有月 椎菜（《Kud Wafter》）"],
                "03-26": ["松岡 チロル（《Heaven Burns Red》）"],
                "03-27": ["鳳 咲夜（《Rewrite》）"],
                "03-30": ["西园美鸟（《Little Busters》）"],
                "04-01": ["あーちゃん先輩《Little Busters!》）,豊後 弥生（《Heaven Burns Red》）"],
                "04-02": ["藤川 みあ（《LOOPERS》）"],
                "04-03": ["相楽 美佐枝（《CLANNAD》）"],
                "04-04": ["久島 鴎（《Summer Pockets》）"],
                "04-05": ["神北 小毬（《Little Busters!》）"],
                "04-08": ["ビャッコ（《Heaven Burns Red》）"],
                "04-13": ["柳 美音（《Heaven Burns Red》）"],
                "04-18": ["北川 潤（《Kanon》"],
                "04-29": ["水織 静久（《Summer Pockets》）"],
                "04-30": ["宮沢 謙吾（《Little Busters!》）"],
                "05-01": ["岡崎 直幸（《CLANNAD》）"],
                "05-02": ["天王寺 瑚太朗（《Rewrite》）"],
                "05-04": ["棗 恭介（《Little Busters!》）"],
                "05-05": ["倉田 佐祐理（《Kanon》）"],
                "05-07": ["シャルロッタ・ スコポフスカヤ（《Heaven Burns Red》）"],
                "05-08": ["利田 美咲（《LOOPERS》）"],
                "05-12": ["室伏 理沙（《Heaven Burns Red》）"],
                "05-13": ["一ノ瀬 ことみ（《CLANNAD》）"],
                "05-21": ["鷹原 羽依里（《Summer Pockets》）"],
                "05-26": ["石井 色葉（《Heaven Burns Red》）"],
                "06-06": ["霧島 譲（《LOOPERS》）,二階堂 三郷（《Heaven Burns Red》）"],
                "06-08": ["鳴瀬 しろは（《Summer Pockets》）"],
                "06-11": ["春原 芽衣（《CLANNAD》）"],
                "06-12": ["霧島 佳乃（《AIR》）,能美 クドリャフカ（《Little Busters!》）"],
                "06-13": ["しまこ（《Rewrite》）"],
                "06-18": ["蔵 里見（《Heaven Burns Red》）,中津 静流（《Rewrite》）"],
                "06-24": ["茅森 月歌（《Heaven Burns Red》）"],
                "06-29": ["桜庭 星羅（《Heaven Burns Red》）"],
                "07-04": ["神山 識（《Summer Pockets》）"],
                "07-07": ["蒼井 えりか（《Heaven Burns Red》）"],
                "07-11": ["朝倉 可憐（《Heaven Burns Red》"],
                "07-12": ["西九条 灯花（《Rewrite》）"],
                "07-16": ["有月 初（《Kud Wafter》）"],
                "07-20": ["古河 秋生（《CLANNAD》）,伊吹 風子（《CLANNAD》）"],
                "07-21": ["平良 明（《LOOPERS》）"],
                "07-22": ["天音 巫呼（《Heaven Burns Red》）"],
                "07-23": ["神尾 観鈴（《AIR》）"],
                "07-26": ["神戸 小鳥（《Rewrite》）"],
                "08-02": ["キャロル・リーパー（《Heaven Burns Red》）"],
                "08-07": ["宮沢 有紀寧（《CLANNAD》）"],
                "08-15": ["夏目 祈（《Heaven Burns Red》）"],
                "08-22": ["西園 美魚（《Little Busters!》）"],
                "08-24": ["鳳 ちはや（《Rewrite》）"],
                "08-25": ["山脇・ボン・ イヴァール（《Heaven Burns Red》）"],
                "08-27": ["幸村 俊夫《CLANNAD》）"],
                "08-31": ["紬 ヴェンダース（《Summer Pockets》）"],
                "09-01": ["加藤 うみ（《Summer Pockets》）"],
                "09-02": ["棗 鈴（《Little Busters!》）"],
                "09-06": ["水瀬 すもも（《Heaven Burns Red》）"],
                "09-09": ["藤林 杏（《CLANNAD》）,藤林 椋《CLANNAD》）"],
                "09-13": ["昼田 貴理子（《LOOPERS》）"],
                "09-14": ["国崎往人（《AIR》）"],
                "09-17": ["和泉 ユキ（《Heaven Burns Red》）"],
                "09-20": ["空門 藍（《Summer Pockets》）,空門 蒼（《Summer Pockets》）"],
                "09-23": ["水瀬 秋子（《Kanon》）"],
                "10-01": ["丸山 奏多（《Heaven Burns Red》）"],
                "10-05": ["古河 早苗（《CLANNAD》）"],
                "10-07": ["アイリーン・ レドメイン（《Heaven Burns Red》）"],
                "10-10": ["加納 天善（《Summer Pockets》）"],
                "10-13": ["二木 佳奈多（《Little Busters!》）,三枝 葉留佳（《Little Busters!》）"],
                "10-14": ["坂上 智代（《CLANNAD》）"],
                "10-18": ["岬 鏡子（《Summer Pockets》）"],
                "10-21": ["伊達 朱里（《Heaven Burns Red》）,朱鷺戸 沙耶（《Little Busters!》）"],
                "10-28": ["逢川 めぐみ（《Heaven Burns Red》）"],
                "10-30": ["岡崎 朋也（《CLANNAD》）"],
                "11-01": ["國見 タマ（《Heaven Burns Red》）"],
                "11-02": ["瑞原 あいな《Heaven Burns Red》）"],
                "11-03": ["氷室 憂希《Kud Wafter》）,神尾 晴子（《AIR》）"],
                "11-06": ["井ノ原 真人（《Little Busters!》）"],
                "11-07": ["吉野 晴彦《Rewrite》）"],
                "11-08": ["樋口 聖華（《Heaven Burns Red》）"],
                "11-22": ["黒沢 真希（《Heaven Burns Red》"],
                "11-29": ["大島 一千子,大島 二以奈,大島 三野里,大島 四ツ葉,大島 五十鈴,大島 六宇亜《Heaven Burns Red》）"],
                "12-01": ["月城 最中（《Heaven Burns Red》）"],
                "12-02": ["鳴瀬 小鳩（《Summer Pockets》）"],
                "12-03": ["笹瀬川 佐々美（《Little Busters!》）"],
                "12-05": ["芳野 祐介（《CLANNAD》）"],
                "12-06": ["天野 美汐（《Kanon》）"],
                "12-14": ["李映夏《Heaven Burns Red》）"],
                "12-15": ["神奈 备命（《AIR》）"],
                "12-22": ["遠野 美凪《AIR》）"],
                "12-23": ["此花 ルチア（《Rewrite》）,水瀬 名雪《Kanon》）"],
                "12-24": ["古河 渚（《CLANNAD》）"],
                "12-25": ["菅原 千恵（《Heaven Burns Red》）"],
                "12-27": ["西森 柚咲（《Charlotte》）,堀井 佐奈（《LOOPERS》）"],

                # 继续添加其他月份的生日信息...
            }

            if today in birthdays:
                names = ", ".join(birthdays[today])
                await message.reply(content=f"今天是 {names} 的生日，生日快乐！")
            else:
                await message.reply(content="今天没有人过生日。")

        elif re.search(r'\b睡觉\b', message.content):
            await asyncio.sleep(10)
        elif re.search(r'\b你好\b', message.content):
            await message.reply(content="你好呀！")
        elif re.search(r'\b吃掉\b', message.content):
            await message.reply(content="吃葡叶了！救命啊!")
        elif re.search(r'\bping\b', message.content):
            await message.reply(content="pong!")
        elif re.search(r'\b晚安\b', message.content):
            await message.reply(content="晚安,宝宝。")

        elif re.search(r'\b一月份生日名单\b', message.content):
            await message.reply(content="\
                   雾岛 聖（《AIR》），birthday: '01-03'\n\
                   桐生 美也（《Heaven Burns Red》），birthday: '01-05'\n\
                   泽渡 真琴（《Kanon》），birthday: '01-06'\n\
                   白河 ユイナ（《Heaven Burns Red》），birthday: '01-06'\n\
                   月宫 あゆ（《Kanon》），birthday: '01-07'\n\
                   直枝架夜（《Kud Wafter》），birthday: '01-12'\n\
                   水濑 いちご（《Heaven Burns Red》），birthday: '01-15'\n\
                   直枝 理树（《Little Busters》），birthday: '01-17'\n\
                   伊吹 公子（《CLANNAD》），birthday: '01-18'\n\
                   LUNAR-Q（《LUNARiA》），birthday: '01-23'\n\
                   ヴリティカ・ バラクリシュナン（《Heaven Burns Red》），birthday: '01-26'\n\
                   川澄 舞（《Kanon》），birthday: '01-29'")

        elif re.search(r'\b二月份生日名单\b', message.content):
            await message.reply(content="\
                   美坂 栞（《Kanon》）, birthday: '02-01'\n\
                   岡崎 汐（《CLANNAD》）, birthday: '02-01' \n\
                   野村 美希（《Summer Pockets》）, birthday: '02-02'\n\
                   佐月 マリ（《Heaven Burns Red》）, birthday: '02-07'\n\
                   三谷 良一（《Summer Pockets》）, birthday: '02-09'\n\
                   東城 つかさ（《Heaven Burns Red》）, birthday: '02-14'\n\
                   千里 朱音（《Rewrite》）, birthday: '02-17'\n\
                   春原 陽平（《CLANNAD》）, birthday: '02-17'\n\
                   神崎 アーデルハイド（《Heaven Burns Red》）, birthday: '02-22' \n\
                   町村 玲央奈（《LOOPERS》）, birthday: '02-24' \n\
                   マリア・デ・ アンジェリス（《Heaven Burns Red》）, birthday: '02-26' ")

        elif re.search(r'\b三月份生日名单\b', message.content):
            await message.reply(content="\
                   美坂 香里（《Kanon》）, birthday: '03-01' \n\
                   命 吹雪（《Heaven Burns Red》）, birthday: '03-04' \n\
                   西門 貴明（《LOOPERS》）, birthday: '03-05' \n\
                   井上 晶（《Rewrite》）, birthday: '03-06' \n\
                   来ヶ谷 唯湖（《Little Busters!》）, birthday: '03-13'\n\
                   柊木 梢（《Heaven Burns Red》）, birthday: '03-18' \n\
                   小笠原 緋雨（《Heaven Burns Red》）, birthday: '03-21'\n\
                   有月 椎菜（《Kud Wafter》）, birthday: '03-25'\n\
                   松岡 チロル（《Heaven Burns Red》）, birthday: '03-26'\n\
                   鳳 咲夜（《Rewrite》）, birthday: '03-27' \n\
                   西园美鸟（《Little Busters》）, birthday: '03-30'")

        elif re.search(r'\b四月份生日名单\b', message.content):
            await message.reply(content="\
                   あーちゃん先輩《Little Busters!》）, birthday: '04-01'\n\
                   豊後 弥生（《Heaven Burns Red》）', birthday: '04-01'\n\
                   藤川 みあ（《LOOPERS》）, birthday: '04-02'\n\
                   相楽 美佐枝（《CLANNAD》）, birthday: '04-03'\n\
                   久島 鴎（《Summer Pockets》）, birthday: '04-04'\n\
                   神北 小毬（《Little Busters!》）, birthday: '04-05'\n\
                   ビャッコ（《Heaven Burns Red》）, birthday: '04-08'\n\
                   柳 美音（《Heaven Burns Red》）, birthday: '04-13'\n\
                   北川 潤（《Kanon》）, birthday: '04-18' \n\
                   水織 静久（《Summer Pockets》）, birthday: '04-29'\n\
                   宮沢 謙吾（《Little Busters!》）, birthday: '04-30'")

        elif re.search(r'\b五月份生日名单\b', message.content):
            await message.reply(content="\
                   岡崎 直幸（《CLANNAD》）, birthday: '05-01'\n\
                   天王寺 瑚太朗（《Rewrite》）, birthday: '05-02'\n\
                   棗 恭介（《Little Busters!》）, birthday: '05-04'\n\
                   倉田 佐祐理（《Kanon》）, birthday: '05-05'\n\
                   シャルロッタ・ スコポフスカヤ（《Heaven Burns Red》）, birthday: '05-07'\n\
                   利田 美咲（《LOOPERS》）, birthday: '05-08'\n\
                   室伏 理沙（《Heaven Burns Red》）, birthday: '05-12'\n\
                   一ノ瀬 ことみ（《CLANNAD》）, birthday: '05-13'\n\
                   鷹原 羽依里（《Summer Pockets》）, birthday: '05-21'\n\
                   石井 色葉（《Heaven Burns Red》）, birthday: '05-26'")

        elif re.search(r'\b六月份生日名单\b', message.content):
            await message.reply(content="\
                   霧島 譲（《LOOPERS》）, birthday: '06-06'\n\
                   二階堂 三郷（《Heaven Burns Red》）, birthday: '06-06'\n\
                   鳴瀬 しろは（《Summer Pockets》）, birthday: '06-08'\n\
                   春原 芽衣（《CLANNAD》）, birthday: '06-11'\n\
                   霧島 佳乃（《AIR》）, birthday: '06-12'\n\
                   能美 クドリャフカ（《Little Busters!》）, birthday: '06-12'\n\
                   しまこ（《Rewrite》）, birthday: '06-13'\n\
                   蔵 里見（《Heaven Burns Red》）, birthday: '06-18'\n\
                   中津 静流（《Rewrite》）, birthday: '06-18'\n\
                   茅森 月歌（《Heaven Burns Red》）, birthday: '06-24'\n\
                   桜庭 星羅（《Heaven Burns Red》）, birthday: '06-29'")

        elif re.search(r'\b七月份生日名单\b', message.content):
            await message.reply(content="\
                   神山 識（《Summer Pockets》）, birthday: '07-04'\n\
                   蒼井 えりか（《Heaven Burns Red》）, birthday: '07-07'\n\
                   朝倉 可憐（《Heaven Burns Red》）, birthday: '07-11'\n\
                   西九条 灯花（《Rewrite》）, birthday: '07-12'\n\
                   有月 初（《Kud Wafter》）, birthday: '07-16'\n\
                   古河 秋生（《CLANNAD》）, birthday: '07-20'\n\
                   伊吹 風子（《CLANNAD》）, birthday: '07-20'\n\
                   平良 明（《LOOPERS》）, birthday: '07-21'\n\
                   天音 巫呼（《Heaven Burns Red》）, birthday: '07-22'\n\
                   神尾 観鈴（《AIR》）, birthday: '07-23'\n\
                   神戸 小鳥（《Rewrite》）, birthday: '07-26'")

        elif re.search(r'\b八月份生日名单\b', message.content):
            await message.reply(content="\
                   キャロル・リーパー（《Heaven Burns Red》）, birthday: '08-02'\n\
                   宮沢 有紀寧（《CLANNAD》）, birthday: '08-07'\n\
                   夏目 祈（《Heaven Burns Red》）, birthday: '08-15'\n\
                   西園 美魚（《Little Busters!》）, birthday: '08-22'\n\
                   鳳 ちはや（《Rewrite》）, birthday: '08-24'\n\
                   山脇・ボン・ イヴァール（《Heaven Burns Red》）, birthday: '08-25'\n\
                   幸村 俊夫《CLANNAD》）, birthday: '08-27'\n\
                   紬 ヴェンダース（《Summer Pockets》）, birthday: '08-31'")

        elif re.search(r'\b九月份生日名单\b', message.content):
            await message.reply(content="\
                   加藤 うみ（《Summer Pockets》）, birthday: '09-01'\n\
                   棗 鈴（《Little Busters!》）', birthday: '09-02'\n\
                   水瀬 すもも（《Heaven Burns Red》）', birthday: '09-06'\n\
                   藤林 杏（《CLANNAD》）, birthday: '09-09'\n\
                   藤林 椋《CLANNAD》）, birthday: '09-09'\n\
                   昼田 貴理子（《LOOPERS》）, birthday: '09-13'\n\
                   国崎往人（《AIR》）, birthday: '09-14'\n\
                   和泉 ユキ（《Heaven Burns Red》）, birthday: '09-17'\n\
                   空門 藍（《Summer Pockets》）, birthday: '09-20'\n\
                   空門 蒼（《Summer Pockets》）, birthday: '09-20'\n\
                   水瀬 秋子（《Kanon》）, birthday: '09-23'")

        elif re.search(r'\b十月份生日名单\b', message.content):
            await message.reply(content="\
                   丸山 奏多（《Heaven Burns Red》）', birthday: '10-01'\n\
                   古河 早苗（《CLANNAD》）, birthday: '10-05'\n\
                   アイリーン・ レドメイン（《Heaven Burns Red》）, birthday: '10-07'\n\
                   加納 天善（《Summer Pockets》）, birthday: '10-10'\n\
                   二木 佳奈多（《Little Busters!》）, birthday: '10-13'\n\
                   三枝 葉留佳（《Little Busters!》）, birthday: '10-13'\n\
                   坂上 智代（《CLANNAD》）, birthday: '10-14'\n\
                   岬 鏡子（《Summer Pockets》）, birthday: '10-18'\n\
                   伊達 朱里（《Heaven Burns Red》）, birthday: '10-21'\n\
                   朱鷺戸 沙耶（《Little Busters!》）, birthday: '10-21'\n\
                   逢川 めぐみ（《Heaven Burns Red》）, birthday: '10-28'\n\
                   岡崎 朋也（《CLANNAD》）, birthday: '10-30'")

        elif re.search(r'\b十一月份生日名单\b', message.content):
            await message.reply(content="\
                   國見 タマ（《Heaven Burns Red》）, birthday: '11-01'\n\
                   瑞原 あいな《Heaven Burns Red》）, birthday: '11-02'\n\
                   氷室 憂希《Kud Wafter》）, birthday: '11-03'\n\
                   神尾 晴子（《AIR》）, birthday: '11-03'\n\
                   井ノ原 真人（《Little Busters!》）, birthday: '11-06'\n\
                   吉野 晴彦《Rewrite》）, birthday: '11-07'\n\
                   樋口 聖華（《Heaven Burns Red》）, birthday: '11-08'\n\
                   黒沢 真希（《Heaven Burns Red》）, birthday: '11-22'\n\
                   大島 一千子（《Heaven Burns Red》）, birthday: '11-29'\n\
                   大島 二以奈（《Heaven Burns Red》）, birthday: '11-29'\n\
                   大島 三野里（《Heaven Burns Red》）, birthday: '11-29'\n\
                   大島 四ツ葉（《Heaven Burns Red》）, birthday: '11-29'\n\
                   大島 五十鈴（《Heaven Burns Red》）, birthday: '11-29'\n\
                   大島 六宇亜（《Heaven Burns Red》）, birthday: '11-29'")

        elif re.search(r'\b十二月份生日名单\b', message.content):
            await message.reply(content="\
                   月城 最中（《Heaven Burns Red》）, birthday: '12-01'\n\
                   鳴瀬 小鳩（《Summer Pockets》）, birthday: '12-02'\n\
                   笹瀬川 佐々美（《Little Busters!》）, birthday: '12-03'\n\
                   芳野 祐介（《CLANNAD》）, birthday: '12-05'\n\
                   天野 美汐（《Kanon》）, birthday: '12-06'\n\
                   李映夏《Heaven Burns Red》）, birthday: '12-14'\n\
                   神奈 备命（《AIR》）, birthday: '12-15'\n\
                   遠野 美凪《AIR》）, birthday: '12-22'\n\
                   此花 ルチア（《Rewrite》）, birthday: '12-23'\n\
                   水瀬 名雪《Kanon》）, birthday: '12-23'\n\
                   古河 渚（《CLANNAD》）, birthday: '12-24'\n\
                   菅原 千恵（《Heaven Burns Red》）, birthday: '12-25'\n\
                   西森 柚咲（《Charlotte》）, birthday: '12-27'\n\
                   堀井 佐奈（《LOOPERS》）, birthday: '12-27'")


        else:

            # 使用 GLM-4 模型生成回答

            input_text = message.content

            client = ZhipuAI(api_key="xxxxxxxxxxxxxxxxxx")  # 请填写您自己的APIKey

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
