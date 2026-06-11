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
| GET | `/api/words` | 词条列表，支持 `?region=四川` 按地区筛选、`?keyword=巴适` 关键词模糊匹配（方言词或普通话），两个参数可单独或组合使用 |
| GET | `/api/words/random` | 随机获取一条词条 |
| GET | `/api/words/:id` | 词条详情 |
| POST | `/api/words` | 新增词条 |
| POST | `/api/words/batch-delete` | 批量删除词条 |
| PUT | `/api/words/:id` | 更新词条 |
| DELETE | `/api/words/:id` | 删除词条 |
| GET | `/api/regions` | 地区列表（去重） |
| GET | `/api/stats/region` | 按地区统计词条数量 |

### 查询全部词条接口

**路径**：`GET /api/words`

返回所有词条，支持地区筛选与关键词搜索两个可选查询参数，两个参数可单独使用或任意组合。

**查询参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `region` | `string` | 否 | 按地区精确筛选，如 `四川` |
| `keyword` | `string` | 否 | 关键词模糊匹配，同时作用于「方言词」和「普通话」两个字段 |

**示例请求**：

```
# 仅按地区筛选
GET /api/words?region=四川

# 仅关键词搜索
GET /api/words?keyword=巴适

# 地区 + 关键词组合
GET /api/words?region=四川&keyword=巴适
```

### 随机获取词条接口

**路径**：`GET /api/words/random`

从数据库中随机返回一条完整词条记录。

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | `number` | 词条 ID |
| `dialect_word` | `string` | 方言词 |
| `mandarin` | `string` | 对应普通话释义 |
| `region` | `string` | 所属地区 |
| `example` | `string` | 例句（可能为空字符串） |
| `source` | `string` | 来源（可能为空字符串） |
| `remark` | `string` | 备注（可能为空字符串） |

响应示例：
```json
{
  "id": 3,
  "dialect_word": "巴适",
  "mandarin": "舒适、好",
  "region": "四川",
  "example": "这个火锅真巴适！",
  "source": "",
  "remark": ""
}
```

> 当数据库中无任何词条时，返回 `404` 状态码及 `{"error": "暂无词条数据"}`。

### 按地区统计接口返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | `number` | 全库词条总条数 |
| `regions` | `array` | 各地区统计数组 |
| `regions[].region` | `string` | 地区名称 |
| `regions[].count` | `number` | 该地区词条数量 |

响应示例：
```json
{
  "total": 100,
  "regions": [
    { "region": "四川", "count": 30 },
    { "region": "广东", "count": 25 }
  ]
}
```

### 批量删除词条接口

**路径**：`POST /api/words/batch-delete`

接收词条编号数组，一次性删除多条记录，返回实际删除成功的条数。

**请求参数**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ids` | `array` | 是 | 要删除的词条编号数组，如 `[1, 2, 3]` |

**返回字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `deleted_count` | `number` | 实际删除成功的词条数量 |

请求示例：
```json
{
  "ids": [1, 2, 3]
}
```

响应示例：
```json
{
  "deleted_count": 3
}
```

> 如果传入的编号不存在或无效，`deleted_count` 会返回实际成功删除的条数。

## 页面入口

| 页面 | 路径 | 说明 |
|------|------|------|
| 词汇列表 | `/` | 首页，展示所有词条，支持搜索和地区筛选 |
| 每日一词 | `/daily` | 随机学词页面，大号字体展示词条，提供「换一条」按钮重新获取 |
| 数据统计 | `/stats` | 地区统计看板，页头显示全库总条数，表格展示各地区词条数量 |
| 新增词条 | `/words/new` | 新增方言词条表单 |
| 词条详情 | `/words/:id` | 查看和编辑指定词条 |

每日一词页面和数据统计页面可通过应用头部导航的对应按钮进入。

## 数据字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `dialect_word` | `string` | 是 | 方言词 |
| `mandarin` | `string` | 是 | 对应普通话 |
| `region` | `string` | 是 | 地区 |
| `example` | `string` | 否 | 例句 |
| `source` | `string` | 否 | 来源 |
| `remark` | `string` | 否 | 备注，可选文字说明 |

## Seed 数据

首次启动自动插入 5 条示例词条（江西、广东、四川、上海、陕西各一条）。
