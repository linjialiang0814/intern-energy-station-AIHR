# 方案说明

本项目为“实习能量站：AI 驱动的业务部实习生成长导航智能看板”。问题诊断：业务部实习生分布在研发、产品、销售等岗位，带教质量依赖导师经验；实习生不知道 30-60-90 天每阶段该学什么、交付什么；HR 和招聘同学难以及时掌握整体进度、风险和适岗情况。

方案设计面向 HR、导师、实习生、招聘同学四类角色，提供五个模块：HR Dashboard 展示 20 名实习生的任务分、适岗分、风险分布、Top/Bottom 排名和导出；Intern Profile 展示个人画像、评分解释、任务记录和风险行动建议；Mentor Assistant 将导师自然语言反馈结构化为优点、问题、风险、带教动作和反馈话术，并支持写入 SQLite；Intern Growth Assistant 根据岗位、周次和能力短板生成本周建议与 30-60-90 天成长路径；AI Weekly Report 自动生成 HR 周报和风险名单。

AI 工具选型采用“规则模型 + LLM 增强 + fallback”架构。适岗评分和风险等级用可解释规则保证稳定性，权重为任务完成度 30%、导师评价 25%、学习主动性 20%、沟通协作 15%、岗位技能 10%。导师反馈分析、成长建议和周报支持火山引擎方舟 OpenAI 兼容接口；未配置 API Key 或请求失败时自动使用模板 fallback，保证在线 Demo 可演示。

关键配置包括 CSV 模拟数据、SQLite 数据层、角色权限矩阵、评分权重、风险关键词、Prompt 模板、Streamlit Cloud 部署和 GitHub Actions。项目迭代从 MVP 看板开始，逐步补齐模拟数据、评分规则、个人画像、导师反馈分析、周报生成、LLM 接入、导出能力、pytest/CI、SQLite 持久化和角色视角。

效果评估通过一键质量检查完成：数据聚合、评分解释、AI fallback、导出、SQLite 保存、角色权限均有脚本或 pytest 验证。当前 Demo 已形成“整体态势 -> 风险定位 -> 个人画像 -> 反馈分析 -> 成长路径 -> 周报输出”闭环，并部署至 Streamlit Cloud：https://intern-energy-station-linjialiang.streamlit.app/。项目Github网址：https://github.com/linjialiang0814/intern-energy-station-AIHR。
