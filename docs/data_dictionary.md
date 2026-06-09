# 数据字典

## interns.csv

| 字段 | 含义 |
| --- | --- |
| intern_id | 实习生唯一 ID |
| name | 实习生姓名 |
| role | 岗位类型：研发、产品、销售 |
| school | 学校 |
| major | 专业 |
| mentor_id | 导师 ID |
| join_date | 入职日期 |
| current_week | 当前实习周数 |
| status | 状态 |

## mentors.csv

| 字段 | 含义 |
| --- | --- |
| mentor_id | 导师唯一 ID |
| mentor_name | 导师姓名 |
| department | 所属部门 |
| role | 导师岗位 |

## weekly_tasks.csv

| 字段 | 含义 |
| --- | --- |
| task_id | 任务 ID |
| role | 适用岗位 |
| week | 适用周次 |
| task_name | 任务名称 |
| task_description | 任务说明 |
| expected_output | 预期交付物 |
| weight | 任务权重 |

## intern_progress.csv

| 字段 | 含义 |
| --- | --- |
| intern_id | 实习生 ID |
| task_id | 任务 ID |
| week | 周次 |
| completion_status | 完成状态 |
| completion_score | 完成分 |
| submission_text | 提交说明 |
| updated_at | 更新时间 |

## mentor_feedback.csv

| 字段 | 含义 |
| --- | --- |
| feedback_id | 反馈 ID |
| intern_id | 实习生 ID |
| mentor_id | 导师 ID |
| week | 周次 |
| feedback_text | 导师自然语言反馈 |
| professional_score | 专业能力评分 |
| communication_score | 沟通协作评分 |
| initiative_score | 学习主动性评分 |
| created_at | 创建时间 |

## evaluation_results.csv

| 字段 | 含义 |
| --- | --- |
| intern_id | 实习生 ID |
| week | 周次 |
| task_score | 任务完成度评分 |
| mentor_score | 导师综合评分 |
| initiative_score | 学习主动性评分 |
| communication_score | 沟通协作评分 |
| skill_match_score | 岗位技能匹配评分 |
| fit_score | 适岗度总分 |
| level | 适岗等级 |
| risk_level | 风险等级 |
| ai_summary | 面向 HR 的摘要建议 |
