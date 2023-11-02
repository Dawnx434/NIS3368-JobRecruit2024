# -*- coding: utf-8 -*-
import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.Edge()
position_names = ['行政助理/行政助理','销售代表/销售经理','人力资源经理/人力资源助理','财务分析师/财务经理','市场营销经理/市场营销专员','客户服务代表/客户服务经理','软件工程师/软件开发经理','数据分析师/数据科学家','项目经理/项目协调员','运营经理/运营助理']
position_descriptions = ['行政助理/行政助理：负责协助管理和组织日常办公室事务，包括文件处理、会议安排、行程管理和协调部门之间的沟通。','销售代表/销售经理：负责销售产品或服务，与客户建立联系，提供产品信息，处理销售订单和达成销售目标。','人力资源经理/人力资源助理：管理组织的人力资源策略和实践，包括招聘、培训、员工关系、绩效评估和员工福利等方面的工作。','财务分析师/财务经理：负责分析和解释财务数据，制定预算和财务计划，评估投资机会，提供财务建议和支持战略决策。','市场营销经理/市场营销专员：开展市场调研，制定市场营销策略，执行市场推广活动，管理品牌形象，与客户建立关系并推动产品销售。','客户服务代表/客户服务经理：处理客户的问题和投诉，提供产品或服务的支持和解决方案，确保客户满意度和维护良好的客户关系。','软件工程师/软件开发经理：设计、开发和测试软件程序，参与软件项目的规划和管理，解决技术问题，并确保软件的高质量和按时交付。','数据分析师/数据科学家：收集、整理和分析数据，提取有价值的信息和见解，应用统计和机器学习技术进行数据建模和预测，支持业务决策。','项目经理/项目协调员：规划、执行和监督项目，确保项目按时、按质量和预算完成，协调团队成员、资源和沟通，解决项目中的问题。','运营经理/运营助理：负责组织和管理日常运营活动，包括供应链管理、生产计划、库存控制、流程改进和质量管理等方面的工作。']
# 打开目标网页
cookies = [

    {
        'name': 'sessionid',
        'value': '0dct4m43v69bonil6u4nqp54kkfauuti',

    },
]
driver.get("http://127.0.0.1:8000/position/publish/")
# Add each cookie to the WebDriver
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get("http://127.0.0.1:8000/position/publish/")
for i in range(14):
    driver.get("http://127.0.0.1:8000/position/publish/")
    position_name_place = driver.find_element(By.ID, 'position_name')
    position_name_place.send_keys(position_names[i])
    salary = driver.find_element(By.ID,'salary')
    salary.send_keys('10000')
    summary = driver.find_element(By.ID,'summary')
    summary.send_keys(position_names[i])
    # 输入职位详细信息
    detail = driver.find_element(By.XPATH,'/html/body/div/div/div/form/fieldset/div[4]/div[2]/div[6]')
    actions = ActionChains(driver)
    actions.click(detail).send_keys(position_descriptions[i]).perform()
    city = driver.find_element(By.ID,'district')
    drop_down = Select(city)
    drop_down.select_by_index(random.randint(0,950))
    # 选择已发布
    publish = driver.find_element(By.ID, 'published_state')
    drop_down = Select(publish)
    drop_down.select_by_index(1)
    # 点击提交
    button = driver.find_element(By.XPATH,'/html/body/div/div/div/form/fieldset/button')
    # 这里加载一会以免被覆盖
    time.sleep(1)
    button.click()

