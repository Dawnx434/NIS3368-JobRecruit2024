# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.Edge()
names = [' 投资记录贴——跬步千里 ',' 李尚福被免去国防部长和国务委员职务 秦刚被免去国务委员职务', '自动化就业薪资？',' 歧视第一学历，是在扼杀年轻人向上的底气','所剩无几的校园日记（随缘找工作专心写论文版）',' 拼多多技术岗校招','国家统计局：9月份全国城镇调查失业率平均为5.0%','两三年后的就业形势到底会怎么样啊']
details = ['去年在各个帖子下零零散散地记录过一些投机想法，后来随着生活忙碌潦草收尾逐渐淡出，在水不在深的帖子里遗留了不少坑。最近每天都跟长辈打电话交流股市，但交流的内容不久便置之脑后，lz深感记忆力不够用，希望今后通过公开记录的方式，督促自己记录每个短周期内对形势的观测、形成决策的依据，通过不定期的回溯反思自己决策依据的合理性，不断优化自己的决策能力。最后，这个帖子只记录个人的所思所想所感，欢迎讨论，切忌跟随。','据央视《新闻联播》报道,李尚福被免去国务委员、国防部部长职务,秦刚被免去国务委员职务','电院分流，鼠鼠去自动化了。在水源上看到有人说自动化平均薪资甚至不如电气，感到异常害怕。（为功利之心流下眼泪）有没有自动化的学长学姐分享一下自动化本科和研究生就业平均薪资是多少啊。','他是懂欺软怕硬的，今年的年轻人失业率是多少呀','学生时代只剩不到一年了，今年还遭受了一些大的变故和变动，是时候要调整好心态，积极地走下去啦！今年的目标：好好吃饭好好运动好好学习找个好工作不找男人第1和2条是因为余老扁的内分泌十分紊乱嘞，有过服药调理的经历，于是胖了...接下来想要靠健康饮食和规律运动来减肥，以期内分泌能正常起来。今年一定要把肥减下来！第3和4条是因为余老扁今年年底就要毕业答辩咯，也马上要面临找工作的问题，还是想回快乐老家，感觉很安心，亲人和最好的朋友也都在老家。第5条，这几年男人运太差(可能我自己状态也不好吧)，谈了也白谈，想遇见个正常的人好好谈下去的...算命的说我晚婚，30岁之后 :sob:欢迎走进我的生活，但别 :package:我，我社恐。（8.03更新：其实也已经盒了不少了）','拼多多校招内推，组内十分缺人，私聊我简历可直达大leader :rofl:学弟学妹们冲冲冲（我已经呆了3年了，体验看部门，我自己还可以的）','澎湃，澎湃新闻，澎湃新闻网，新闻与思想，澎湃是植根于中国上海的时政思想类互联网平台，以最活跃的原创新闻与最冷静的思想分析为两翼，是互联网技术创新与新闻价值传承的结合体，致力于问答式新闻与新闻追踪功能的实践','这段时间很关注这个话题感觉什么观点都有（我检讨这是一句废话水源的友友们怎么看这个问题啊（纯粹友好探讨 我是小白 没有观点倾向没有观点倾向没有观点倾向']
# 打开目标网页
cookies = [

    {
        'name': 'sessionid',
        'value': '',

    },
]
driver.get("http://127.0.0.1:8000/new_topic/")
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get("http://127.0.0.1:8000/new_topic/")
for i in range(7):
    driver.get("http://127.0.0.1:8000/new_topic/")
    name = driver.find_element(By.XPATH,'//*[@id="id_subject"]')
    name.send_keys(names[i])
    # 输入职位详细信息
    detail = driver.find_element(By.XPATH, '/html/body/div/div/form/div[2]/div[3]/div[6]')
    actions = ActionChains(driver)
    actions.click(detail).send_keys(details[i]).perform()
    # 点击提交
    button = driver.find_element(By.XPATH, '/html/body/div/div/form/button')
    # 这里加载一会以免被覆盖
    time.sleep(1)
    # 强制通过 JavaScript 执行按钮点击
    driver.execute_script("arguments[0].click();", button)
    # button.click()
