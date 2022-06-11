# -*- encoding: utf-8 -*-
'''
    __                __                      __          ____             _     __             ____                    __      __
   / /   ___   ___   / /_  _____  ____   ____/ /  ___    / __ \  ____ _   (_)   / /   __  __   / __ \   _____  ____    / /_    / /  ___    ____ ___
  / /   / _ \ / _ \ / __/ / ___/ / __ \ / __  /  / _ \  / / / / / __ `/  / /   / /   / / / /  / /_/ /  / ___/ / __ \  / __ \  / /  / _ \  / __ `__ \
 / /___/  __//  __// /_  / /__  / /_/ // /_/ /  /  __/ / /_/ / / /_/ /  / /   / /   / /_/ /  / ____/  / /    / /_/ / / /_/ / / /  /  __/ / / / / / /
/_____/\___/ \___/ \__/  \___/  \____/ \__,_/   \___/ /_____/  \__,_/  /_/   /_/    \__, /  /_/      /_/     \____/ /_.___/ /_/   \___/ /_/ /_/ /_/
                                                                                   /____/
@File      :   LeetcodeDailyProblem.main.py
@Author    :   Cute_CAT
@Contact   :   2971504919@qq.com
'''
import OlivOS
import LeetcodeDailyProblem
import httpx
import aiohttp
import asyncio
import re
import json

class Event(object):
    def init(plugin_event, Proc):
        pass

    def init_after(plugin_event, Proc):
        pass

    def private_message(plugin_event, Proc):
        unit_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        unit_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        pass

Headers = {
    "origin": "https://leetcode-cn.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

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

def unit_reply(plugin_event, Proc):
    if plugin_event.data.message == '每日一题':
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        task = loop.create_task(get_leetcode_daily())
        loop.run_until_complete(task)
        reply_js = task.result()
        reply_str = '今日力扣每日一题\n' + '编号：' + reply_js['id'] + '\n题目：' + reply_js['title'] + '\n难度：' + reply_js[
            'difficulty'] + '\n描述：' + reply_js['content'] + '\n链接：' + reply_js['url']
        plugin_event.reply(reply_str)

