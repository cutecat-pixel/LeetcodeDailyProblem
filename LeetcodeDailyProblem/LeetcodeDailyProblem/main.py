import datetime

import OlivOS
import LeetcodeDailyProblem
from datetime import date
import httpx
import aiohttp
import asyncio
import re
import json
import os
import threading

class Event(object):
    def init(plugin_event, Proc):
        if not os.path.exists("plugin/data/LeetcodeDailyProblem"):
            os.mkdir("plugin/data/LeetcodeDailyProblem")
        try:
            with open("plugin/data/LeetcodeDailyProblem/Data.json", "r", encoding="utf-8") as file:
                json.load(file)
        except:
            data = {'date': [' ']}
            with open("plugin/data/LeetcodeDailyProblem/Data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

    def init_after(plugin_event, Proc):
        peek_thread = MyThread(Proc)
        peek_thread.start()

    def private_message(plugin_event, Proc):
        pass

    def group_message(plugin_event, Proc):
        pass

    def save(plugin_event, Proc):
        pass

Headers = {
    "origin": "https://leetcode-cn.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}
botHash = '4e551e7f45b823887df833fc20dafa2d'

async def get_leetcode_daily() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post("https://leetcode-cn.com/graphql", json={"operationName": "questionOfToday", "variables": {}, "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"}, headers=Headers, timeout=5) as response:
            RawData = await response.json(content_type=None)
            EnglishTitle = RawData["data"]["todayRecord"][0]["question"]["questionTitleSlug"]
            QuestionUrl = f"https://leetcode-cn.com/problems/{EnglishTitle}"
        async with session.post("https://leetcode-cn.com/graphql", json={"operationName": "questionData", "variables": {"titleSlug": EnglishTitle}, "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"}, headers=Headers, timeout=5) as response:
            RawData = await response.json(content_type=None)
            Data = RawData["data"]["question"]
            ID = Data["questionFrontendId"]
            Difficulty = Data["difficulty"]
            ChineseTitle = Data["translatedTitle"]
            Content = re.sub(r"(<\w+>|</\w+>)", "", Data["translatedContent"]).replace("&nbsp;", "").replace("&lt;", "<").replace("\t", "").replace("\n\n", "\n").replace("\n\n", "\n")
            Data = {"id": ID, "title": ChineseTitle, "difficulty": Difficulty, "content": Content, "url": QuestionUrl}
            return Data

class MyThread(threading.Thread):
    def __init__(self, Proc):
        super().__init__()
        self.Proc = Proc

    def run(self):
        while True:
            with open("plugin/data/LeetcodeDailyProblem/Data.json", "r", encoding="utf-8") as file:
                time_js = json.load(file)
            if time_js['date'] == [] or time_js['date'][0] == ' ':
                with open("plugin/data/LeetcodeDailyProblem/Data.json", "w", encoding="utf-8") as file:
                    time_js['date'][0] = str(datetime.date.today())
                    json.dump(time_js, file, indent=4, ensure_ascii=False)
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    loop = asyncio.get_event_loop()
                    task = loop.create_task(get_leetcode_daily())
                    loop.run_until_complete(task)
                    reply_js = task.result()
                    reply_str = '今日力扣每日一题\n' + '编号' + reply_js['id'] + '\n题目：' + reply_js['title'] + '\n难度：' + reply_js[
                        'difficulty'] + '\n描述：' + reply_js['content'] + '\n链接：' + reply_js['url']
                    plugin_event = OlivOS.API.Event(
                        OlivOS.contentAPI.fake_sdk_event(
                            bot_info=self.Proc.Proc_data['bot_info_dict'][botHash],
                            fakename='OlivOSLive'
                        ),
                        self.Proc.log
                    )
                    plugin_event.send('group', 7236694, reply_str)
            elif str(datetime.date.today()) != time_js['date'][0]:
                with open("plugin/data/LeetcodeDailyProblem/Data.json", "w", encoding="utf-8") as file:
                    if datetime.datetime.now().hour == 8:
                        time_js['date'][0] = str(datetime.date.today())
                        json.dump(time_js, file, indent=4, ensure_ascii=False)
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        loop = asyncio.get_event_loop()
                        task = loop.create_task(get_leetcode_daily())
                        loop.run_until_complete(task)
                        reply_js = task.result()
                        reply_str = '今日力扣每日一题\n' + '编号' + reply_js['id'] + '\n题目：' + reply_js['title'] + '\n难度：' + reply_js['difficulty'] + '\n描述：' + reply_js['content'] + '\n链接：' + reply_js['url']
                        plugin_event = OlivOS.API.Event(
                            OlivOS.contentAPI.fake_sdk_event(
                                bot_info=self.Proc.Proc_data['bot_info_dict'][botHash],
                                fakename='OlivOSLive'
                            ),
                            self.Proc.log
                        )
                        plugin_event.send('group', 7236694, reply_str)
