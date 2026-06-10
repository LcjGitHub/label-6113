# 方言词汇库 MVP

前后端分离的方言词汇管理应用：词汇列表（地区筛选）+ 词条详情/编辑，基础 CRUD。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + TypeScript + Element Plus（端口 **4101**） |
| 后端 | Flask 3 + Flask-Cors + SQLAlchemy（端口 **4000**） |
| 数据库 | SQLite `./backend/instance/dialect.db` |

## 目录结构

```
.
├── backend/          # Flask API
│   ├── app.py
│   ├── models.py
│   ├── seed.py
│   ├── requirements.txt
│   └── instance/     # SQLite 数据库（首次启动自动创建）
└── frontend/         # Vue 3 前端
    ├── src/
    └── package.json
```

## 快速启动

### 1. 后端（端口 4000）

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

后端启动后访问 `http://localhost:4000/api/words` 可查看词条列表。首次运行会自动创建数据库并写入 5 条 seed 数据。

### 2. 前端（端口 4101）

另开一个终端：

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:4101`。

> 前端通过 Vite 代理将 `/api` 请求转发到 `http://localhost:4000`，请先启动后端。

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/words` | 词条列表，支持 `?region=四川` 筛选 |
| GET | `/api/words/:id` | 词条详情 |
| POST | `/api/words` | 新增词条 |
| PUT | `/api/words/:id` | 更新词条 |
| DELETE | `/api/words/:id` | 删除词条 |
| GET | `/api/regions` | 地区列表（去重） |

## 数据字段

- **方言词** `dialect_word`
- **普通话** `mandarin`
- **地区** `region`
- **例句** `example`
- **来源** `source`

## Seed 数据

首次启动自动插入 5 条示例词条（江西、广东、四川、上海、陕西各一条）。
