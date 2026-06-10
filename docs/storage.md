# SQLite 数据持久化说明

第三阶段开始，项目支持从 CSV 种子数据初始化 SQLite，并支持导师反馈持久化。

## 数据库位置

默认数据库文件：

```text
data/intern_energy_station.db
```

该文件属于运行时数据，已加入 `.gitignore`，不会提交到 GitHub。

## 初始化数据库

```bash
python scripts/init_db.py
```

如果需要从 CSV 重新生成数据库：

```bash
python scripts/init_db.py --force
```

## 数据读取策略

`services/data_service.py` 会优先读取 SQLite。若 SQLite 不存在，会自动从 CSV 初始化。若初始化失败，则回退读取 CSV，保证 Demo 不会因为数据库问题无法启动。

## 导师反馈持久化

在 `Mentor Assistant` 页面中，导师输入反馈后可以点击“保存导师反馈”。

保存后：

- `mentor_feedback` 表会更新该实习生的最新反馈。
- `mentor_feedback_history` 表会追加一条历史记录。
- 个人画像和周报会读取最新反馈。

## 当前限制

- Streamlit Cloud 的本地 SQLite 更适合 Demo，不适合长期多用户生产数据存储。
- 如果要正式生产化，建议迁移到 PostgreSQL，并增加角色权限与审计日志。
