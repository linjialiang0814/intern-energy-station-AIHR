一个工程化、可落地、能做出完整 Demo 的项目架构与执行计划。该方案围绕作业四「实习能量站」展开，目标是解决导师带教不标准、实习生不知道学什么、HR 和招聘同学难以及时掌握适岗情况的问题。题目要求是设计一套“业务部实习生成长导航”智能工具，并交付可运行 Demo、公网链接和 1000 字以内方案说明。

一、项目定位

项目名称建议：

Intern Energy Station：AI 驱动的实习生成长导航与适岗评估系统

一句话定位：

面向 HR、业务导师、实习生和招聘团队，提供实习生成长路径规划、导师带教建议、风险预警、适岗度评估和 AI 周报生成的一体化智能看板。

核心价值不是“做一个聊天机器人”，而是做一个 AI + HR 数据产品：

HR 能看全局情况；
导师能获得标准化带教建议；
实习生能知道自己每周该学什么；
招聘同学能查看适岗度和转正潜力；
AI 能把分散反馈转化为结构化结论和行动建议。
二、推荐技术栈

考虑课程作业需要快速交付、可运行、易部署，推荐使用轻量但工程化的架构。

方案 A：最快可交付版本

适合 3-5 天内完成。

Frontend + Backend:
Streamlit

Data:
CSV / JSON 模拟数据

AI:
OpenAI / DeepSeek / 通义千问 / 豆包 API

Deployment:
Streamlit Cloud / Hugging Face Spaces

优点：开发快、页面和图表一体化、适合 Demo 展示。

缺点：工程复杂度不如前后端分离。

方案 B：更工程化版本

适合 5-10 天完成，展示效果更像真实产品。

Frontend:
Vue 3 + Element Plus / React + Ant Design

Backend:
FastAPI

Database:
SQLite / PostgreSQL

AI Layer:
LLM API + Prompt Templates

Visualization:
ECharts

Deployment:
Vercel + Render / Railway

优点：架构完整，适合展示工程能力。

缺点：开发成本更高。

推荐选择

如果你主要目标是课程作业拿高分，我建议选择：

Streamlit + SQLite/CSV + LLM API + Plotly 图表 + 公网部署

它兼顾了工程化结构和交付效率。

三、系统总体架构

可以设计为五层架构：

用户层
  ├── HR
  ├── 导师
  ├── 实习生
  └── 招聘同学

应用层
  ├── HR 总览看板
  ├── 实习生个人成长页
  ├── 导师带教助手
  ├── 实习生 AI 成长助手
  ├── 适岗度评估模块
  └── AI 周报生成模块

服务层
  ├── 成长路径生成服务
  ├── 反馈结构化服务
  ├── 风险识别服务
  ├── 适岗评分服务
  ├── 推荐建议生成服务
  └── 周报生成服务

AI 层
  ├── Prompt 模板
  ├── LLM 调用
  ├── 结构化输出解析
  └── 规则 + AI 混合决策

数据层
  ├── 实习生基础信息表
  ├── 岗位成长任务表
  ├── 导师反馈表
  ├── 实习生周报表
  ├── 评分结果表
  └── 风险记录表
四、核心功能模块设计
1. HR 总览看板

HR 首页是整个 Demo 的门面，建议优先做漂亮。

展示内容
实习生总数：20
岗位分布：研发 / 产品 / 销售
高潜人数：5
正常成长人数：11
需关注人数：4
平均任务完成率：76%
导师反馈提交率：85%
平均适岗度：78.5
本周风险预警：4 条
图表建议
图表	用途
岗位分布饼图	展示 20 名实习生分布
任务完成率柱状图	对比研发、产品、销售进度
适岗度排名表	展示 Top / Bottom 实习生
风险等级分布图	展示低/中/高风险人数
能力雷达图	展示单个实习生能力画像
HR 可执行动作

HR 点击某个风险实习生后，可以看到：

风险原因：
- 连续两周任务完成率低于 60%
- 导师反馈中出现“主动性不足”
- 自评中出现“对工作方向不清楚”

AI 建议：
- 建议 HR 安排一次 15 分钟沟通
- 建议导师下周提供更明确的任务目标
- 建议为该实习生补充岗位学习路径
2. 实习生个人成长页

每个实习生拥有一个个人档案页。

页面字段
姓名：李明
岗位：研发实习生
导师：王老师
当前周数：第 3 周
任务完成率：70%
适岗度评分：82
风险等级：低风险
推荐结论：稳定培养
能力维度

建议设置 5 个维度：

维度	含义
专业技能	岗位相关硬技能
学习主动性	是否主动学习、主动提问
沟通协作	和导师、团队的配合程度
业务理解	对部门业务和岗位目标的理解
任务交付	是否能按时完成任务
AI 输出
AI 成长建议：
李明目前在任务交付和专业技能方面表现较好，但业务理解仍处于建立阶段。
建议下周参与一次需求评审，并完成一份模块功能说明文档，以增强对业务流程的理解。
3. 导师带教助手

这是最能体现 AI 价值的模块之一。

输入

导师输入一段自然语言反馈：

小王这周完成了接口文档阅读，也能独立跑通测试环境。
但是代码提交较少，开会时比较沉默，不太主动表达问题。
AI 输出
{
  "positive_points": ["完成接口文档阅读", "能独立跑通测试环境"],
  "problems": ["代码实践产出较少", "会议中表达不主动"],
  "risk_level": "medium",
  "mentor_suggestions": [
    "下周安排一个明确的小型代码任务",
    "在每日站会中主动询问其遇到的问题",
    "鼓励其做一次 5 分钟技术分享"
  ],
  "feedback_to_intern": "你本周在环境熟悉和文档学习方面表现不错。下周可以尝试承担一个小型开发任务，并在遇到问题时更主动地和导师沟通。"
}
工程实现

后端可以设计一个函数：

def analyze_mentor_feedback(feedback_text: str, intern_profile: dict) -> dict:
    """
    输入导师自然语言反馈，输出结构化评价、风险等级和带教建议。
    """

如果不接真实 LLM，也可以先用关键词规则模拟：

积极关键词：完成、主动、独立、优秀、清晰、按时
风险关键词：拖延、沉默、不主动、迷茫、缺席、质量差

但建议至少接入一次 LLM API，这样 Demo 更有说服力。

4. 实习生 AI 成长助手

实习生可以向系统提问：

我是产品岗实习生，现在第 2 周，我应该重点学什么？

系统结合岗位、阶段和当前表现生成建议：

你现在处于产品岗实习第 2 周，建议重点完成三个目标：

1. 熟悉业务流程：阅读部门已有 PRD 和需求评审记录。
2. 建立产品分析能力：选择一个竞品，完成一页竞品分析。
3. 主动对齐导师预期：和导师确认本月需要产出的具体成果。

本周建议交付物：
- 一份竞品分析表
- 一份业务流程图
- 一次与导师的阶段沟通记录

这个模块适合放在右侧 Chatbot 区域。

5. 适岗度评分模块

适岗度评分要做到 可解释，不要只有一个分数。

评分公式

建议使用规则评分 + AI 解释。

总分 = 任务完成度 × 30%
     + 导师评价 × 25%
     + 学习主动性 × 20%
     + 沟通协作 × 15%
     + 岗位技能匹配 × 10%
等级划分
分数	等级	解释
85-100	高潜	可重点培养，具备转正潜力
70-84	稳定	表现正常，可继续观察
60-69	需关注	存在短板，需要导师干预
0-59	高风险	可能不适岗，需要 HR 跟进
输出示例
适岗度：82 / 100
等级：稳定

评分解释：
该实习生任务完成率较高，导师评价整体正向，说明基础能力较稳定。
但学习主动性和业务理解分数略低，建议下阶段增加主动汇报和业务分析任务。
6. AI 周报生成模块

HR 一键生成本周实习生管理周报。

输入数据
20 名实习生的任务完成率
导师反馈
风险等级
适岗评分
岗位分布
本周变化趋势
输出内容
本周实习生整体表现稳定。20 名实习生中，5 人为高潜，11 人正常成长，4 人需要重点关注。

从岗位看，研发岗任务完成率最高，平均为 82%；产品岗业务理解提升较快；销售岗个体差异较大，有 2 名同学出现主动性不足的问题。

建议下周重点采取三项行动：
1. HR 跟进 4 名中高风险实习生；
2. 导师补齐 3 份缺失的周反馈；
3. 为销售岗实习生增加标准化客户沟通训练任务。

这是最终演示时非常加分的功能。

五、数据模型设计

即使使用 CSV，也要设计得像真实数据库。

1. interns 表
intern_id
name
role
school
major
mentor_id
join_date
current_week
status

示例：

intern_id,name,role,school,major,mentor_id,current_week,status
I001,李明,研发,南京大学,计算机科学,M001,3,active
I002,王雨,产品,中山大学,信息管理,M002,2,active
I003,陈晨,销售,武汉大学,市场营销,M003,4,active
2. mentors 表
mentor_id
mentor_name
department
role
3. weekly_tasks 表
task_id
role
week
task_name
task_description
expected_output
weight

示例：

task_id,role,week,task_name,expected_output,weight
T001,研发,1,完成开发环境配置,环境截图与运行记录,20
T002,研发,2,阅读项目代码结构,代码结构说明文档,30
T003,产品,1,阅读已有PRD,PRD阅读笔记,20
T004,销售,1,熟悉产品卖点,产品卖点总结,20
4. intern_progress 表
intern_id
task_id
completion_status
completion_score
submission_text
updated_at
5. mentor_feedback 表
feedback_id
intern_id
mentor_id
week
feedback_text
professional_score
communication_score
initiative_score
created_at
6. evaluation_results 表
intern_id
week
task_score
mentor_score
initiative_score
communication_score
skill_match_score
fit_score
risk_level
ai_summary
六、项目目录结构

如果用 Streamlit，建议这样组织：

intern-energy-station/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── interns.csv
│   ├── mentors.csv
│   ├── weekly_tasks.csv
│   ├── intern_progress.csv
│   ├── mentor_feedback.csv
│   └── evaluation_results.csv
│
├── pages/
│   ├── 1_HR_Dashboard.py
│   ├── 2_Intern_Profile.py
│   ├── 3_Mentor_Assistant.py
│   ├── 4_Intern_Growth_Assistant.py
│   └── 5_AI_Weekly_Report.py
│
├── services/
│   ├── data_service.py
│   ├── scoring_service.py
│   ├── risk_service.py
│   ├── llm_service.py
│   └── report_service.py
│
├── prompts/
│   ├── mentor_feedback_prompt.txt
│   ├── growth_plan_prompt.txt
│   ├── weekly_report_prompt.txt
│   └── fit_score_explanation_prompt.txt
│
├── utils/
│   ├── charts.py
│   ├── constants.py
│   └── validators.py
│
└── docs/
    ├── solution_description.md
    ├── demo_script.md
    └── screenshots/
七、核心后端服务设计
1. data_service.py

负责读取和合并数据。

def load_interns():
    pass

def load_mentor_feedback():
    pass

def get_intern_profile(intern_id):
    pass

def get_intern_weekly_progress(intern_id):
    pass
2. scoring_service.py

负责适岗度评分。

def calculate_fit_score(record):
    task_score = record["task_score"] * 0.30
    mentor_score = record["mentor_score"] * 0.25
    initiative_score = record["initiative_score"] * 0.20
    communication_score = record["communication_score"] * 0.15
    skill_score = record["skill_match_score"] * 0.10

    total = task_score + mentor_score + initiative_score + communication_score + skill_score
    return round(total, 2)
3. risk_service.py

负责风险识别。

def classify_risk(fit_score, task_completion, mentor_feedback_text):
    risk_keywords = ["不主动", "拖延", "迷茫", "缺席", "质量较低", "沟通不足"]

    keyword_hit = any(word in mentor_feedback_text for word in risk_keywords)

    if fit_score < 60 or task_completion < 50:
        return "高风险"
    elif fit_score < 70 or keyword_hit:
        return "需关注"
    else:
        return "低风险"
4. llm_service.py

负责统一调用大模型。

def call_llm(prompt: str) -> str:
    """
    调用大模型 API。
    为了避免 Demo 失败，可以设置 fallback：
    如果 API 调用失败，则返回规则生成的默认结果。
    """
5. report_service.py

负责生成 HR 周报。

def generate_weekly_report(summary_data):
    prompt = build_weekly_report_prompt(summary_data)
    return call_llm(prompt)
八、Prompt 模板设计
1. 导师反馈结构化 Prompt
你是一个 HR 实习生带教分析助手。
请根据导师反馈，提取实习生的优点、问题、风险等级和下周带教建议。

要求：
1. 输出 JSON 格式；
2. 风险等级只能是 low、medium、high；
3. 建议要具体、可执行；
4. 语气专业、温和。

实习生信息：
{intern_profile}

导师反馈：
{feedback_text}

请输出：
{
  "strengths": [],
  "weaknesses": [],
  "risk_level": "",
  "mentor_actions": [],
  "message_to_intern": ""
}
2. 成长路径生成 Prompt
你是一个企业 HR 培养专家。
请为以下实习生生成下一周成长计划。

岗位：{role}
当前周数：{week}
当前任务完成率：{completion_rate}
能力短板：{weaknesses}

请输出：
1. 本周学习重点；
2. 推荐任务；
3. 建议交付物；
4. 需要主动向导师确认的问题；
5. 一句鼓励性反馈。
3. 适岗评分解释 Prompt
你是一个 HR 人才评估助手。
请根据以下评分结果，生成适岗度解释。

任务完成度：{task_score}
导师评价：{mentor_score}
学习主动性：{initiative_score}
沟通协作：{communication_score}
岗位技能匹配：{skill_score}
总分：{fit_score}
等级：{level}

要求：
1. 解释为什么是这个等级；
2. 指出 1-2 个优势；
3. 指出 1-2 个改进方向；
4. 给出下一步行动建议。
4. HR 周报 Prompt
你是 HR 数据分析助手。
请根据以下实习生群体数据，生成一份本周实习生成长周报。

数据：
{summary_data}

要求：
1. 总结整体情况；
2. 分析不同岗位表现；
3. 标出重点风险；
4. 给出下周行动建议；
5. 语言简洁，适合发给 HR 和业务负责人。
九、页面设计方案
页面 1：首页 / 项目介绍

内容：

Intern Energy Station
AI 驱动的实习生成长导航与适岗评估系统

核心功能：
- HR 总览看板
- 实习生个人成长画像
- 导师反馈智能分析
- 实习生 AI 成长助手
- 适岗度评分与风险预警
- AI 周报生成
页面 2：HR 总览看板

布局：

顶部：核心指标卡片
中间：岗位分布图 + 风险分布图
下方：实习生适岗度排名表
右侧：AI 总结与行动建议
页面 3：实习生画像

布局：

左侧：选择实习生
中间：基础信息 + 成长进度
右侧：能力雷达图 + AI 成长建议
下方：任务完成记录 + 导师反馈记录
页面 4：导师带教助手

布局：

选择实习生
输入导师反馈
点击“AI 分析”
输出结构化分析
输出下周带教建议
输出可复制的反馈话术
页面 5：实习生 AI 成长助手

布局：

选择岗位
选择当前周数
输入困惑
点击生成建议
输出学习重点、推荐任务、交付物、导师沟通问题
页面 6：AI 周报

布局：

选择周次
点击生成周报
展示：
- 总体概况
- 岗位分析
- 风险名单
- 下周行动建议
十、开发执行计划
第 1 阶段：需求拆解与数据准备

目标：明确产品边界，准备模拟数据。

任务：

确定用户角色：HR、导师、实习生、招聘同学；
确定核心功能：看板、画像、反馈分析、成长助手、周报；
构造 20 名实习生模拟数据；
构造研发、产品、销售三类岗位任务；
构造导师反馈文本；
设计评分权重和风险规则。

交付物：

data/interns.csv
data/weekly_tasks.csv
data/mentor_feedback.csv
data/evaluation_results.csv
第 2 阶段：基础 Demo 搭建

目标：先做出一个能跑的系统。

任务：

初始化 Streamlit 项目；
实现页面导航；
实现数据读取；
实现 HR Dashboard；
实现实习生列表和详情页；
实现基础图表。

交付物：

app.py
pages/1_HR_Dashboard.py
pages/2_Intern_Profile.py

这一阶段完成后，系统已经可以展示。

第 3 阶段：评分与风险模块

目标：让系统具备“判断能力”。

任务：

实现适岗度评分公式；
实现风险等级判断；
实现高潜 / 稳定 / 需关注 / 高风险分类；
在看板和个人页中展示评分结果；
对风险对象生成行动建议。

交付物：

services/scoring_service.py
services/risk_service.py
第 4 阶段：AI 能力接入

目标：让系统从普通看板升级为 AI 工具。

任务：

实现 LLM API 调用；
设计 Prompt 模板；
实现导师反馈结构化；
实现成长建议生成；
实现适岗评分解释；
实现 HR 周报生成；
加入 API 失败 fallback，避免演示崩溃。

交付物：

services/llm_service.py
services/report_service.py
prompts/*.txt
第 5 阶段：页面美化与演示优化

目标：提升展示效果。

任务：

优化首页介绍；
优化核心指标卡片；
增加图表；
增加 AI 输出区域；
增加风险标签颜色；
加入示例输入按钮；
准备演示路径。

演示路径建议：

1. 打开首页，介绍项目目标；
2. 进入 HR 看板，展示 20 名实习生整体情况；
3. 点击一个风险实习生，查看个人画像；
4. 进入导师助手，输入导师反馈；
5. 展示 AI 结构化分析和带教建议；
6. 进入实习生成长助手，生成个人成长计划；
7. 进入 AI 周报，一键生成 HR 周报。
第 6 阶段：部署与交付材料

目标：形成完整课程交付物。

任务：

部署到 Streamlit Cloud / Hugging Face Spaces；
写 README；
写 1000 字以内方案说明；
截图保存；
录制 3 分钟演示视频。

交付物：

公网 Demo 链接
solution_description.pdf / docx
demo_video.mp4
GitHub 仓库链接
十一、MVP 与增强版范围

为了避免做得过大，可以分成 MVP 和增强版。

MVP 必做功能
1. HR 总览看板
2. 实习生个人画像
3. 适岗度评分
4. 风险等级识别
5. 导师反馈 AI 分析
6. AI 周报生成

这 6 个功能足够支撑高质量 Demo。

增强功能
1. 实习生 AI 问答助手
2. 30-60-90 天成长路径
3. 多角色登录
4. 数据编辑与保存
5. 历史趋势分析
6. 导师反馈完成率提醒
7. 一键生成转正建议

如果时间不足，不建议做复杂登录系统。可以用侧边栏选择角色来模拟。

十二、评分亮点设计

这个作业要做得出色，建议突出以下 5 个亮点。

亮点 1：多角色协同

不是单一 HR 工具，而是覆盖：

HR：看整体、看风险、看周报
导师：写反馈、拿建议、规范带教
实习生：看路径、看任务、问 AI
招聘同学：看适岗度、看转正潜力

这能直接回应题目中的“提高不同角色之间的协同效率”。

亮点 2：AI 不只是聊天，而是结构化分析

AI 负责把自然语言反馈转成：

优点
问题
风险等级
行动建议
反馈话术
适岗解释

这比普通问答更像真实 HR 产品。

亮点 3：评分可解释

每个适岗分数都能解释来源：

任务完成度为什么高
导师评价为什么中等
主动性哪里不足
下一步怎么提升
亮点 4：从发现问题到推动行动

风险预警后必须给行动建议：

安排 1v1 沟通
补齐导师反馈
增加具体任务
调整带教节奏
补充学习材料
亮点 5：可演示闭环

最终形成完整闭环：

数据输入 → AI 分析 → 看板展示 → 风险识别 → 成长建议 → HR 周报
十三、1000 字方案说明框架

最终提交文档可以写成：

1. 问题诊断
某部门新入职 20 名实习生，导师带教依赖经验，缺少统一节奏；实习生不知道每阶段该学什么；HR 和招聘同学难以及时掌握整体适岗情况。

2. 方案设计
本项目设计“实习能量站”，面向 HR、导师、实习生和招聘同学，提供 HR 总览看板、实习生画像、导师反馈助手、成长建议助手、适岗评分和 AI 周报功能。

3. AI 工具选型
使用大模型处理自然语言导师反馈、生成成长建议、解释适岗评分和生成周报；同时结合规则评分模型，保证结果稳定、可解释。

4. 关键配置
设计任务完成度、导师评价、学习主动性、沟通协作、岗位技能匹配五个评分维度；设置高潜、稳定、需关注、高风险四类等级。

5. 迭代记录
第一版完成数据看板；第二版加入评分和风险预警；第三版接入 AI 反馈分析和周报生成；第四版优化页面和演示流程。

6. 效果评估
通过任务完成率、导师反馈完成率、风险识别数量、AI 建议可采纳性、HR 查看效率等指标评估系统效果。
十四、最终建议的开发顺序

最合理的实现顺序是：

1. 先造 20 名实习生数据
2. 做 HR Dashboard
3. 做个人画像页
4. 做适岗评分和风险规则
5. 做导师反馈 AI 分析
6. 做 AI 周报
7. 做实习生成长助手
8. 美化页面
9. 部署公网
10. 写方案说明和录屏

不要一开始就做登录、数据库权限、复杂工作流。课程作业最重要的是：

可运行、能展示、逻辑完整、AI 价值清楚。

这个项目最终应该被包装成一个完整的 HR 智能数据产品，而不是一个简单聊天工具。这样更容易体现你对 AI+HR 场景的理解，也更容易在作业中做出差异化。