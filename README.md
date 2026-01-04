# NEO Bot Framework

> 🌐 官网: [https://neobot.k2cro4.my/](https://neobot.k2cro4.my/)

## 📖 概述

NEO 是一个基于 Python 的现代化 OneBot 11 协议机器人框架，专为需要高性能、可扩展性和开发效率的团队设计。该框架通过 WebSocket 与各种 OneBot 实现端（如 NapCatQQ、LLOneBot 等）通信，提供了一套完整的机器人开发解决方案。

### 设计理念

NEO 框架的设计遵循以下核心理念：

1.  **开发者友好**：简洁的 API 设计、完整的类型提示和详细的文档，让开发者能够快速上手和高效开发
2.  **架构清晰**：采用模块化设计，分离关注点，使代码易于维护和扩展
3.  **高性能异步**：基于 `asyncio` 和 `websockets` 构建，支持高并发消息处理
4.  **类型安全**：全面使用 Python 类型系统，提供编译时类型检查，减少运行时错误
5.  **热重载支持**：支持插件热重载，开发过程中修改代码无需重启机器人

### 核心价值

- **快速原型开发**：通过简洁的装饰器语法快速定义指令和事件处理器
- **生产环境就绪**：内置断线重连、错误处理和性能监控机制
- **可扩展架构**：支持自定义插件、中间件和权限系统
- **现代化开发体验**：支持热重载、类型提示和完整的 API 文档

### 适用场景

- QQ 群机器人管理
- 自动化客服与问答系统
- 游戏社区管理
- 团队内部工具集成
- 教育与培训辅助

## ✨ 特性

*   **OneBot 11 标准支持**：完整支持 OneBot 11 的消息、通知、请求和元事件。
*   **类型安全**：基于 `dataclasses` 的强类型事件模型，开发体验更佳。
*   **插件系统**：轻量级的装饰器风格插件系统，支持指令 (`@matcher.command`) 和事件监听 (`@matcher.on_notice`, `@matcher.on_request`)。
*   **插件元数据与内置帮助**：插件可通过 `__plugin_meta__` 变量进行自我描述。框架核心内置了 `/help` 指令，可自动收集并展示所有插件的帮助信息，无需手动维护。
*   **🔥 热重载支持**：内置文件监控，修改 `plugins` 下的代码自动重载，无需重启，极大提升调试效率。
*   **异步核心**：基于 `asyncio` 和 `websockets` 的高性能异步核心。
*   **自动重连**：内置 WebSocket 断线重连机制。

## ⚡️ 性能优化

### Redis 缓存机制
为了提升响应速度并减少对 OneBot API 的重复调用，框架核心集成了一套基于 Redis 的缓存系统。对于一些不频繁变更的数据（如群信息、好友列表等），首次查询后会将其缓存至 Redis，在缓存有效期内（默认为 1 小时），后续请求将直接从 Redis 读取，极大提升了性能。

#### 工作原理
- **自动缓存**：框架会自动缓存特定 API 的调用结果。
- **缓存键**：缓存键根据 API 名称和关键参数（如 `group_id`, `user_id`）生成，确保唯一性。
- **过期时间**：默认缓存 1 小时，之后会自动失效，下次调用时将重新从 OneBot 实现端获取最新数据。

#### 受影响的 API
以下核心 API 已默认启用缓存：
- `get_group_info`
- `get_group_member_info`
- `get_friend_list`
- `get_stranger_info`
- `get_login_info`

#### 如何绕过缓存
在某些场景下，你可能需要获取实时数据而非缓存数据。为此，所有受缓存影响的 API 方法都增加了一个 `no_cache: bool = False` 的可选参数。

当你需要强制从服务器获取最新信息时，只需在调用时传入 `no_cache=True` 即可。

**示例：**
```python
# 正常调用，会使用缓存
group_info = await bot.get_group_info(group_id=12345)

# 强制获取最新信息，不使用缓存
latest_group_info = await bot.get_group_info(group_id=12345, no_cache=True)
```

### `__slots__` 内存优化
框架内的所有数据模型（包括事件、消息段、API 返回对象等）均已启用 `__slots__ = True` 优化。这可以显著减少每个对象实例的内存占用，特别是在处理大量事件和数据时，能够有效降低机器人的整体内存消耗。


## 📝 待办事项 (TODO)

### API 封装
- [x] **消息相关**
    - `delete_msg`: 撤回消息
    - `get_msg`: 获取消息
    - `get_forward_msg`: 获取合并转发消息
    - `send_like`: 发送点赞
- [x] **群组管理**
    - `set_group_kick`: 群组踢人
    - `set_group_ban`: 群组单人禁言
    - `set_group_anonymous_ban`: 群组匿名禁言
    - `set_group_whole_ban`: 群组全员禁言
    - `set_group_admin`: 群组设置管理员
    - `set_group_anonymous`: 群组匿名
    - `set_group_card`: 设置群名片（群备注）
    - `set_group_name`: 设置群名
    - `set_group_leave`: 退出群组
    - `set_group_special_title`: 设置群组专属头衔
- [x] **群组信息**
    - `get_group_info`: 获取群信息
    - `get_group_list`: 获取群列表
    - `get_group_member_info`: 获取群成员信息
    - `get_group_member_list`: 获取群成员列表
    - `get_group_honor_info`: 获取群荣誉信息
- [x] **用户相关**
    - `get_login_info`: 获取登录号信息
    - `get_stranger_info`: 获取陌生人信息
    - `get_friend_list`: 获取好友列表
- [x] **请求处理**
    - `set_friend_add_request`: 处理加好友请求
    - `set_group_add_request`: 处理加群请求/邀请
- [x] **系统/其他**
    - `get_version_info`: 获取版本信息
    - `get_status`: 获取状态
    - `can_send_image`: 检查是否可以发送图片
    - `can_send_record`: 检查是否可以发送语音
    - `clean_cache`: 清理缓存

### 待实现 API
- [ ] **Web 凭证类**
    - `get_cookies`
    - `get_csrf_token`
    - `get_credentials`
- [ ] **文件/资源信息**
    - `get_image`
    - `get_record`
    - `get_file`
- [ ] **系统控制**
    - `set_restart`
- [ ] **扩展功能**
    - [x] `send_forward_msg`: 发送合并转发消息

### 其他改进
- [x] **API 强类型封装**: 将 API 返回值从 `dict` 转换为数据模型对象。
- [x] **Redis 支持**: 集成 Redis 连接池，便于插件复用连接。
- [x] **权限系统**: 实现基础的权限管理（超级管理员、群管理员等）。
- [x] **日志系统优化**: 引入 `loguru` 进行日志记录，支持文件输出和日志级别控制。
- [x] **异常处理增强**: 增强插件执行过程中的异常捕获，防止单个插件崩溃影响整个 Bot。
- [x] **中间件支持**: 添加消息处理中间件，支持在指令执行前/后进行拦截和处理。

## 📂 项目结构

```
.
├── plugins/                # 插件目录，新建插件文件即可自动加载（支持热重载）
│   ├── admin.py            # 管理员插件
│   └── echo.py             # 示例插件：实现 /echo 和 /赞我 指令
├── core/                   # 核心框架代码
│   ├── api/                # API 模块抽象层
│   ├── bot.py              # Bot 实例与 API 封装
│   ├── admin_manager.py    # 管理员管理模块
│   ├── command_manager.py  # 命令与事件分发器
│   ├── config_loader.py    # 配置加载器
│   ├── event_handler.py    # 事件处理器
│   ├── executor.py         # 插件执行器
│   ├── logger.py           # 日志系统
│   ├── permission_manager.py # 权限管理器
│   ├── plugin_manager.py   # 插件加载与管理
│   ├── redis_manager.py    # Redis 连接管理器
│   └── ws.py               # WebSocket 客户端核心
├── data/                   # 数据存储目录
│   ├── admin.json          # 管理员配置文件
│   └── permissions.json    # 权限数据
├── models/                 # 数据模型
│   ├── events/             # OneBot 事件定义
│   ├── message.py          # 消息段定义
│   ├── objects.py          # API 返回对象定义
│   └── sender.py           # 发送者定义
├── .gitignore
├── config.toml             # 配置文件
├── main.py                 # 启动入口（包含热重载监控）
└── requirements.txt        # 项目依赖
```

### 目录结构详细说明

#### `plugins/` - 插件目录
- **功能**：存放所有机器人插件，支持热重载机制
- **加载机制**：框架会自动扫描此目录下的所有 `.py` 文件，并作为插件加载
- **插件约定**：每个插件文件应包含 `__plugin_meta__` 字典用于插件元数据定义
- **热重载**：开发过程中修改插件文件会自动触发重载，无需重启机器人
- **内置插件**：
  - `admin.py` - 管理员管理插件，支持动态添加/移除管理员
  - `echo.py` - 示例插件，演示基本指令处理

#### `core/` - 核心框架代码
- `api/` - API 模块抽象层
  - `base.py` - API 基类定义
  - `message.py` - 消息相关 API 封装
  - `group.py` - 群组管理 API 封装
  - `friend.py` - 好友相关 API 封装
  - `account.py` - 账号相关 API 封装
- `bot.py` - Bot 核心类，通过 Mixin 模式继承所有 API 功能，提供统一的调用接口
  - `admin_manager.py` - 管理员管理模块，负责管理员的添加、移除和权限验证
  - `command_manager.py` - 命令与事件分发器，负责注册和处理所有指令和事件
- `config_loader.py` - 配置加载器，读取和解析 `config.toml` 配置文件
- `event_handler.py` - 事件处理器，负责将原始事件转换为类型化事件对象
- `executor.py` - 插件执行器，提供线程池执行环境用于执行同步任务
- `logger.py` - 日志系统，基于 `loguru` 提供高性能日志记录
- `permission_manager.py` - 权限管理器，管理用户权限级别（admin、op、user）
- `plugin_manager.py` - 插件加载与管理，负责插件的扫描、加载和热重载
- `redis_manager.py` - Redis 连接管理器，提供异步 Redis 客户端连接池
- `ws.py` - WebSocket 客户端核心，负责与 OneBot 实现端建立和管理连接

#### `data/` - 数据存储目录
- `admin.json` - 管理员配置文件，存储全局管理员列表
- `permissions.json` - 权限数据文件，存储用户权限映射关系


#### `models/` - 数据模型定义
- `events/` - OneBot 事件定义
  - `base.py` - 事件基类定义
  - `message.py` - 消息事件定义
  - `notice.py` - 通知事件定义
  - `request.py` - 请求事件定义
  - `meta.py` - 元事件定义
  - `factory.py` - 事件工厂类，用于根据 JSON 数据创建对应事件对象
- `message.py` - 消息段定义，支持文本、图片、表情等多种消息类型
- `objects.py` - API 返回对象定义，提供强类型化的 API 响应数据模型
- `sender.py` - 发送者定义，包含用户、群成员等信息

#### 根目录文件
- `.gitignore` - Git 忽略文件配置
- `config.toml` - 主配置文件，包含 WebSocket 连接、机器人指令前缀、Redis 连接等配置
- `main.py` - 程序入口文件，负责初始化插件、启动热重载监控和建立 WebSocket 连接
- `requirements.txt` - Python 依赖包列表

## 🚀 快速开始

### 1. 环境准备

*   Python 3.8+
*   OneBot 11 实现端（推荐 [NapCatQQ](https://github.com/NapNeko/NapCatQQ) 或 LLOneBot）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置文件

修改根目录下的 `config.toml`，配置 WebSocket 连接信息：

```toml
[napcat_ws]
uri = "ws://127.0.0.1:30004"  # OneBot 实现端的 WebSocket 地址
token = "your_token"          # Access Token (如果有)
reconnect_interval = 5        # 断线重连间隔（秒）

[bot]
command = ["/"]               # 指令前缀，支持多个，如 ["/", "#"]
```

### 4. 运行

```bash
python main.py
```

## 🛠️ 开发指南

### 🔥 热重载调试

项目集成了 `watchdog` 文件监控。在开发过程中，你只需要：
1.  保持 `main.py` 运行。
2.  修改或新建 `plugins` 目录下的 `.py` 插件文件。
3.  保存文件。
4.  控制台会自动提示 `[HotReload] 插件重载完成`，新的逻辑立即生效。

### 创建新插件

在 `plugins` 目录下创建一个新的 `.py` 文件（例如 `my_plugin.py`），框架会自动加载它。

### 示例代码

#### 1. 注册消息指令

使用 `@matcher.command("指令名")` 注册指令。

```python
from core.command_manager import matcher
from core.bot import Bot
from models import MessageEvent

# 注册 /hello 指令
@matcher.command("hello")
async def handle_hello(bot: Bot, event: MessageEvent, args: list[str]):
    # args 是去除指令后的参数列表
    await event.reply("你好！这里是 NEO Bot。")
```

#### 2. 监听通知事件

使用 `@matcher.on_notice("通知类型")` 监听通知。

```python
from core.command_manager import matcher
from core.bot import Bot
from models import GroupIncreaseNoticeEvent

# 监听群成员增加事件
@matcher.on_notice("group_increase")
async def welcome_new_member(bot: Bot, event: GroupIncreaseNoticeEvent):
    await bot.send_group_msg(event.group_id, f"欢迎新成员 {event.user_id} 加入！")
```

#### 3. 监听请求事件

使用 `@matcher.on_request("请求类型")` 监听请求。

```python
from core.command_manager import matcher
from core.bot import Bot
from models import FriendRequestEvent

# 自动同意好友请求
@matcher.on_request("friend")
async def auto_approve_friend(bot: Bot, event: FriendRequestEvent):
    await bot.call_api("set_friend_add_request", {
        "flag": event.flag,
        "approve": True
    })
```

#### 4. API 调用方式对比

框架提供两种 API 调用方式：**类型化 API**（推荐）和 **通用 API**（备用）。

##### 方式一：类型化 API（推荐）
对于已封装的 API，框架提供了类型化的方法，返回数据模型对象而非原始字典：

```python
from core.command_manager import matcher
from core.bot import Bot
from models import MessageEvent
from models.objects import Group

@matcher.command("info")
async def get_group_info_typed(bot: Bot, event: MessageEvent, args: list[str]):
    # 使用类型化 API，返回 Group 对象
    group: Group = await bot.get_group_info(event.group_id)
    await event.reply(f"群名：{group.group_name}\n成员数：{group.member_count}\n创建时间：{group.create_time}")
```

##### 方式二：通用 API（备用）
如果框架尚未封装某个 OneBot API，你可以使用 `bot.call_api` 直接调用。这是通用的备用调用方法。

```python
from core.command_manager import matcher
from core.bot import Bot
from models import MessageEvent

@matcher.command("info_legacy")
async def get_group_info_legacy(bot: Bot, event: MessageEvent, args: list[str]):
    # 直接调用 get_group_info API
    # action: API 名称
    # params: API 参数字典
    resp = await bot.call_api("get_group_info", {
        "group_id": event.group_id,
        "no_cache": False
    })
    
    if resp.get("status") == "ok":
        group_name = resp["data"]["group_name"]
        await event.reply(f"当前群名：{group_name}")
```

**建议**：优先使用类型化 API，获得更好的类型安全和代码提示。仅在框架未封装特定 API 时使用通用 API。

## 📖 插件开发指南

### 插件基本结构
一个标准的插件文件应该包含以下部分：
1.  **模块文档字符串**：描述插件功能
2.  **导入必要的模块**：从 `core` 和 `models` 导入所需类
3.  **使用装饰器注册事件处理器**：`@matcher.command()`, `@matcher.on_notice()`, `@matcher.on_request()`
4.  **异步函数实现业务逻辑**：使用 `async def` 定义处理函数

### 插件元数据 (`__plugin_meta__`)
为了实现插件的自动发现和帮助信息的自动生成，框架引入了插件元数据机制。你需要在你的插件模块中定义一个名为 `__plugin_meta__` 的字典。

`load_all_plugins` 函数在加载插件时会自动读取这个变量，并将其注册到 `CommandManager` 中。`/help` 指令会遍历所有已注册的元数据，生成格式化的帮助信息。

一个标准的 `__plugin_meta__` 包含以下字段：

-   `name` (str): 插件的友好名称，例如 "回声"。
-   `description` (str): 对插件功能的简短描述。
-   `usage` (str): 插件的使用方法，可以包含多个指令和它们的说明。

**示例：**
```python
# plugins/echo.py

__plugin_meta__ = {
    "name": "回声与交互",
    "description": "提供 echo 和 赞我 功能",
    "usage": "/echo [内容] - 复读内容\n/赞我 - 让机器人给你点赞",
}
```

### 使用类型化 API
框架现已提供完整的类型化 API 封装，建议优先使用这些封装方法而非原始的 `call_api`：

| API 方法 | 返回类型 | 说明 |
|---------|---------|------|
| `bot.send_group_msg()` | `Message` | 发送群消息 |
| `bot.get_group_info()` | `Group` | 获取群信息 |
| `bot.get_group_member_info()` | `GroupMember` | 获取群成员信息 |
| `bot.get_friend_list()` | `List[Friend]` | 获取好友列表 |
| `bot.get_login_info()` | `LoginInfo` | 获取登录信息 |
| `bot.get_version_info()` | `VersionInfo` | 获取版本信息 |

#### 示例：使用类型化 API 重构群信息查询
```python
from core.command_manager import matcher
from core.bot import Bot
from models import MessageEvent
from models.objects import Group

@matcher.command("group_info")
async def get_group_info_typed(bot: Bot, event: MessageEvent, args: list[str]):
    # 使用类型化 API，返回 Group 对象而非字典
    group: Group = await bot.get_group_info(event.group_id)
    await event.reply(f"群名：{group.group_name}\n成员数：{group.member_count}\n创建时间：{group.create_time}")
```

### 事件处理模式
除了基本的消息指令，还可以处理多种事件类型：

#### 1. 通知事件处理
```python
from models import GroupCardChangeEvent

@matcher.on_notice("group_card")
async def handle_group_card_change(bot: Bot, event: GroupCardChangeEvent):
    # event.card_new 是新名片，event.card_old 是旧名片
    await bot.send_group_msg(event.group_id, f"成员 {event.user_id} 的名片从 '{event.card_old}' 改为 '{event.card_new}'")
```

#### 2. 请求事件处理
```python
from models import GroupRequestEvent

@matcher.on_request("group")
async def handle_group_request(bot: Bot, event: GroupRequestEvent):
    # 根据请求类型处理
    if event.sub_type == "add":
        # 自动同意加群请求
        await bot.set_group_add_request(event.flag, event.sub_type, approve=True)
        await bot.send_group_msg(event.group_id, f"已同意用户 {event.user_id} 的加群请求")
```

### 错误处理
建议在插件中添加适当的错误处理，避免单个插件崩溃影响整个机器人：

```python
@matcher.command("dangerous")
async def dangerous_command(bot: Bot, event: MessageEvent, args: list[str]):
    try:
        # 可能失败的操作
        result = await bot.call_api("some_api", {"param": "value"})
        await event.reply(f"成功：{result}")
    except Exception as e:
        await event.reply(f"执行失败：{str(e)}")
        # 记录日志
        from core.logger import logger
        logger.error(f"插件执行错误：{e}", exc_info=True)
```

### 处理同步阻塞操作
为了保持机器人的响应性，所有可能导致长时间阻塞的同步操作都应该在单独的线程池中执行。框架提供了 `run_in_thread_pool` 函数来简化这一过程。

**示例：执行同步阻塞任务**
```python
from core.command_manager import matcher
from core.bot import Bot
from models import MessageEvent
from core.executor import run_in_thread_pool
import time

# 模拟一个耗时的同步操作
def blocking_task(duration: int):
    time.sleep(duration)
    return f"阻塞任务完成，耗时 {duration} 秒"

@matcher.command("block_test")
async def handle_blocking_test(bot: Bot, event: MessageEvent, args: list[str]):
    if not args or not args[0].isdigit():
        await event.reply("请提供一个数字作为阻塞时间（秒）。例如：/block_test 5")
        return
    
    duration = int(args[0])
    await event.reply(f"开始执行阻塞任务，耗时 {duration} 秒...")
    
    # 将同步阻塞任务放入线程池执行
    result = await run_in_thread_pool(blocking_task, duration)
    await event.reply(result)
```

### 权限管理
框架内置了基于用户角色的权限管理系统，支持 `admin`（超级管理员）、`op`（操作员）、`user`（普通用户）三个权限级别。权限数据存储在 `data/permissions.json` 文件中。

#### 权限级别说明
- **admin**：最高权限，可以执行所有管理命令，包括添加/移除其他管理员
- **op**：操作员权限，可以执行大部分管理命令，但不能修改管理员列表
- **user**：普通用户权限，只能使用基础功能

#### 在插件中使用权限控制
注册命令时可以通过 `permission` 参数指定所需权限级别：

```python
from models import MessageEvent

# 只有管理员可以执行此命令
@matcher.command("admin_only", permission=MessageEvent.ADMIN)
async def admin_command(bot: Bot, event: MessageEvent, args: list[str]):
    await event.reply("此命令仅限管理员使用")

# 操作员及以上权限可以执行
@matcher.command("op_only", permission=MessageEvent.OP)
async def op_command(bot: Bot, event: MessageEvent, args: list[str]):
    await event.reply("此命令需要操作员权限")

# 所有用户都可以执行（默认）
@matcher.command("public")
async def public_command(bot: Bot, event: MessageEvent, args: list[str]):
    await event.reply("所有用户都可以使用此命令")
```

#### 动态权限检查
如果需要更复杂的权限逻辑，可以使用 `override_permission_check=True` 参数，然后在函数中手动检查权限：

```python
@matcher.command(
    "special",
    permission=MessageEvent.OP,
    override_permission_check=True
)
async def special_command(bot: Bot, event: MessageEvent, permission_granted: bool):
    if not permission_granted:
        await event.reply("权限不足！")
        return
    
    # 额外的权限逻辑
    if event.user_id == 123456:
        await event.reply("特殊用户，允许执行")
    else:
        await event.reply("普通用户，拒绝执行")
```

### 使用 Redis 进行数据缓存
框架集成了 Redis 客户端，提供了便捷的异步接口用于数据缓存和持久化。Redis 连接管理器会自动管理连接池，你可以在插件中直接使用。

#### 基本用法
```python
from core.redis_manager import redis_manager

@matcher.command("cache")
async def cache_example(bot: Bot, event: MessageEvent, args: list[str]):
    # 设置缓存
    await redis_manager.set("user:123:name", "张三")
    
    # 获取缓存
    name = await redis_manager.get("user:123:name")
    
    # 设置带过期时间的缓存（单位：秒）
    await redis_manager.setex("temp:data", 3600, "临时数据")
    
    # 删除缓存
    await redis_manager.delete("user:123:name")
    
    await event.reply(f"用户名：{name}")
```

#### 使用哈希表（Hash）
```python
# 设置哈希字段
await redis_manager.hset("user:123", "age", 20)
await redis_manager.hset("user:123", "city", "北京")

# 获取哈希字段
age = await redis_manager.hget("user:123", "age")
user_data = await redis_manager.hgetall("user:123")

# 删除哈希字段
await redis_manager.hdel("user:123", "city")
```

#### 使用列表（List）
```python
# 向列表添加元素
await redis_manager.lpush("recent:actions", "login")
await redis_manager.rpush("recent:actions", "logout")

# 获取列表范围
actions = await redis_manager.lrange("recent:actions", 0, 9)

# 获取列表长度
length = await redis_manager.llen("recent:actions")
```

### 插件数据管理
对于需要持久化存储配置或数据的插件，框架提供了 `PluginDataManager` 类，可以方便地管理 JSON 格式的数据文件。

#### 基本用法
```python
from core.plugin_manager import PluginDataManager

# 初始化数据管理器
data_manager = PluginDataManager("weather_plugin")

@matcher.command("weather_set")
async def set_weather_config(bot: Bot, event: MessageEvent, args: list[str]):
    if len(args) < 2:
        await event.reply("用法：/weather_set <城市> <温度>")
        return
    
    city = args[0]
    temperature = args[1]
    
    # 保存配置
    await data_manager.set(city, temperature)
    await event.reply(f"已设置 {city} 的温度为 {temperature}℃")

@matcher.command("weather_get")
async def get_weather_config(bot: Bot, event: MessageEvent, args: list[str]):
    if not args:
        await event.reply("用法：/weather_get <城市>")
        return
    
    city = args[0]
    
    # 读取配置
    temperature = data_manager.get(city)
    if temperature:
        await event.reply(f"{city} 的温度是 {temperature}℃")
    else:
        await event.reply(f"未找到 {city} 的温度配置")
```

#### 数据文件位置
插件数据文件保存在 `plugins/data/` 目录下，每个插件对应一个独立的 JSON 文件。例如 `weather_plugin` 插件的数据文件为 `plugins/data/weather_plugin.json`。

### 插件开发最佳实践
1.  **单一职责**：每个插件专注于一个功能领域
2.  **错误处理**：妥善处理可能发生的异常
3.  **类型提示**：为函数参数和返回值添加类型提示
4.  **文档完整**：为每个函数添加文档字符串
5.  **性能考虑**：避免在插件中执行耗时同步操作
6.  **资源清理**：必要时使用 `try...finally` 确保资源释放

### 🚀 高性能插件开发规范 (避坑指南)
为了保证整个机器人框架的响应速度和稳定性，所有插件都必须遵循异步、非阻塞的开发原则。任何一个插件中的阻塞操作都可能导致整个机器人卡顿或无响应。

以下是必须遵守的核心规范：

#### 1. 禁止任何形式的同步网络请求
- **错误示范**: 使用 `requests` 库发起网络请求。
  ```python
  import requests
  # 错误！这会阻塞整个程序
  response = requests.get("https://api.example.com") 
  ```
- **正确做法**: 必须使用异步 HTTP 客户端，如 `aiohttp` 或 `httpx`。
  ```python
  import httpx
  # 正确，使用 async with 和 await
  async with httpx.AsyncClient() as client:
      response = await client.get("https://api.example.com")
  ```

#### 2. 禁止使用 `time.sleep()`
- **错误示范**: 使用 `time.sleep()` 进行等待。
  ```python
  import time
  # 错误！这会阻塞事件循环
  time.sleep(5)
  ```
- **正确做法**: 必须使用 `asyncio.sleep()`。
  ```python
  import asyncio
  # 正确，这会将控制权交还给事件循环
  await asyncio.sleep(5)
  ```

#### 3. 谨慎处理文件 I/O
- 对于读写小型、本地文件，直接使用 `with open(...)` 通常是可接受的。
- 但对于大型文件或网络文件系统（NFS）上的文件，同步 I/O 可能会导致明显的阻塞。
- **推荐做法**: 对于可能耗时较长的文件操作，使用 `aiofiles` 库。
  ```python
  import aiofiles
  async with aiofiles.open('large_file.dat', mode='rb') as f:
      contents = await f.read()
  ```

#### 4. 将 CPU 密集型任务移出事件循环
- 如果插件需要执行复杂的计算（例如，图像处理、视频转码、数据分析），这些任务会长时间占用 CPU，同样会阻塞事件循环。
- **正确做法**: 使用 `loop.run_in_executor()` 将这类任务抛到独立的线程池或进程池中执行。
  ```python
  import asyncio

  def cpu_bound_task(data):
      # 这是一个耗时的同步函数
      # ... 进行大量计算 ...
      return "计算结果"

  # 在异步的事件处理器中调用
  loop = asyncio.get_running_loop()
  # `None` 表示使用默认的线程池
  result = await loop.run_in_executor(None, cpu_bound_task, "一些数据")
  await event.reply(result)
  ```

遵循以上规范，可以确保您开发的插件不会成为整个机器人应用的性能瓶颈。

### 示例：完整插件模板
```python
"""
天气查询插件

提供 /weather 指令，查询指定城市的天气信息。
"""
from core.command_manager import matcher
from core.bot import Bot
from models import MessageEvent

# 插件元数据，用于 help 指令
__plugin_meta__ = {
    "name": "天气查询",
    "description": "查询指定城市的天气信息",
    "usage": "/weather [城市名称]",
}

@matcher.command("weather")
async def handle_weather(bot: Bot, event: MessageEvent, args: list[str]):
    """
    查询天气信息

    :param bot: Bot 实例
    :param event: 消息事件对象
    :param args: 指令参数列表（城市名称）
    """
    if not args:
        await event.reply("请输入城市名称，例如：/weather 北京")
        return

    city = " ".join(args)
    try:
        # 这里可以调用天气 API
        weather_info = f"{city} 的天气：晴，25℃"
        await event.reply(weather_info)
    except Exception as e:
        await event.reply(f"查询天气失败：{str(e)}")

# 可以注册多个事件处理器
@matcher.on_notice("group_increase")
async def welcome_new_member(bot: Bot, event):
    await bot.send_group_msg(event.group_id, f"欢迎新成员 {event.user_id} 加入！")
```

## 📚 事件模型说明

NEO 框架的事件模型是基于 OneBot v11 协议的强类型数据模型，采用 `dataclasses` 和类型注解构建。所有事件都继承自 `OneBotEvent` 基类，并通过事件工厂自动从 JSON 数据创建对应的事件对象。

### 事件层次结构

```
OneBotEvent (抽象基类)
├── MetaEvent (元事件)
│   ├── HeartbeatEvent (心跳事件)
│   └── LifeCycleEvent (生命周期事件)
├── MessageEvent (消息事件)
│   ├── PrivateMessageEvent (私聊消息事件)
│   └── GroupMessageEvent (群聊消息事件)
├── NoticeEvent (通知事件)
│   ├── FriendAddNoticeEvent (好友添加通知)
│   ├── FriendRecallNoticeEvent (好友消息撤回通知)
│   ├── GroupRecallNoticeEvent (群消息撤回通知)
│   ├── GroupIncreaseNoticeEvent (群成员增加通知)
│   ├── GroupDecreaseNoticeEvent (群成员减少通知)
│   ├── GroupAdminNoticeEvent (群管理员变动通知)
│   ├── GroupBanNoticeEvent (群禁言通知)
│   ├── GroupUploadNoticeEvent (群文件上传通知)
│   ├── PokeNotifyEvent (戳一戳通知)
│   ├── LuckyKingNotifyEvent (运气王通知)
│   ├── HonorNotifyEvent (群荣誉变更通知)
│   ├── GroupCardNoticeEvent (群成员名片更新通知)
│   ├── OfflineFileNoticeEvent (离线文件通知)
│   ├── ClientStatusNoticeEvent (客户端状态变更通知)
│   └── EssenceNoticeEvent (精华消息变动通知)
└── RequestEvent (请求事件)
    ├── FriendRequestEvent (加好友请求)
    └── GroupRequestEvent (加群请求/邀请)
```

### 事件基类：OneBotEvent

所有事件的基类，定义了事件的通用属性和方法：

```python
@dataclass(slots=True)
class OneBotEvent(ABC):
    """
    OneBot v11 事件的抽象基类。
    
    Attributes:
        time (int): 事件发生的时间戳 (秒)
        self_id (int): 收到事件的机器人 QQ 号
        _bot (Optional[Bot]): 内部持有的 Bot 实例引用
    """
    time: int
    self_id: int
    _bot: Optional["Bot"] = field(default=None, init=False)
    
    @property
    @abstractmethod
    def post_type(self) -> str:
        """事件的上报类型，子类必须重写此属性"""
        pass
    
    @property
    def bot(self) -> "Bot":
        """获取与此事件关联的 Bot 实例"""
        if self._bot is None:
            raise ValueError("Bot instance not set for this event")
        return self._bot
    
    @bot.setter
    def bot(self, value: "Bot"):
        """为事件对象设置关联的 Bot 实例"""
        self._bot = value
```

### 事件类型常量

框架定义了完整的事件类型常量，用于标识不同种类的事件：

```python
class EventType:
    META = 'meta_event'        # 元事件：心跳、生命周期等
    REQUEST = 'request       ' # 请求事件：加好友请求、加群请求等
    NOTICE = 'notice'          # 通知事件：群成员增加、文件上传等
    MESSAGE = 'message'        # 消息事件：私聊消息、群消息等
    MESSAGE_SENT = 'message_sent'  # 消息发送事件：机器人自己发送消息的上报
```

### 消息事件

消息事件是机器人最常处理的事件类型，框架提供了完整的消息段支持和便捷的回复方法：

#### MessageEvent (消息事件基类)

```python
@dataclass
class MessageEvent(OneBotEvent):
    message_type: str          # 消息类型: private (私聊), group (群聊)
    sub_type: str              # 消息子类型
    message_id: int            # 消息 ID
    user_id: int               # 发送者 QQ 号
    message: List[MessageSegment]  # 消息内容列表
    raw_message: str           # 原始消息内容
    font: int                  # 字体
    sender: Optional[Sender] #   发送者信息
    
    @property
    def post_type(self) -> str:
        return EventType.MESSAGE
    
    async def reply(self, message: str, auto_escape: bool = False):
        """回复消息（抽象方法，由子类实现）"""
        raise NotImplementedError
```

#### PrivateMessageEvent (私聊消息事件)

```python
@dataclass
class PrivateMessageEvent(MessageEvent):
    async def reply(self, message: str, auto_escape: bool = False):
        """回复私聊消息"""
        await self.bot.send_private_msg(
            user_id=self.user_id, message=message, auto_escape=auto_escape
        )
```

#### GroupMessageEvent (群聊消息事件)

```python
@dataclass
class GroupMessageEvent(MessageEvent):
    group_id: int = 0                     # 群号
    anonymous: Optional[Anonymous] = None # 匿名信息
    
    async def reply(self, message: str, auto_escape: bool = False):
        """回复群聊消息"""
        await self.bot.send_group_msg(
            group_id=self.group_id, message=message, auto_escape=auto_escape
        )
```

### 通知事件

通知事件用于处理各种系统通知，如群成员变动、文件上传等：

#### 常用通知事件示例

```python
@dataclass
class GroupIncreaseNoticeEvent(GroupNoticeEvent):
    """群成员增加通知"""
    operator_id: int = 0      # 操作者 QQ 号
    sub_type: str = ""        # 子类型: approve (管理员同意入群), invite (管理员邀请入群)

@dataclass
class GroupRecallNoticeEvent(GroupNoticeEvent):
    """群消息撤回通知"""
    operator_id: int = 0      # 操作者 QQ 号
    message_id: int = 0       # 被撤回的消息 ID

@dataclass
class PokeNotifyEvent(NotifyNoticeEvent):
    """戳一戳通知"""
    target_id: int = 0        # 被戳者 QQ 号
    group_id: int = 0         # 群号 (如果是群内戳一戳)
```

### 请求事件

请求事件用于处理用户的主动请求，如加好友、加群等：

```python
@dataclass
class FriendRequestEvent(RequestEvent):
    """加好友请求事件"""
    user_id: int = 0          # 发送请求的 QQ 号
    comment: str = ""         # 验证信息
    flag: str = ""            # 请求 flag，用于 API 调用

@dataclass
class GroupRequestEvent(RequestEvent):
    """加群请求/邀请事件"""
    sub_type: str = ""        # 子类型: add (加群请求), invite (邀请登录号入群)
    group_id: int = 0         # 群号
    user_id: int = 0          # 发送请求的 QQ 号
    comment: str = ""         # 验证信息
    flag: str = ""            # 请求 flag，用于 API 调用
```

### 元事件

元事件用于处理框架自身状态变化，如心跳、生命周期等：

```python
@dataclass
class HeartbeatEvent(MetaEvent):
    """心跳事件，用于确认连接状态"""
    meta_event_type: str = 'heartbeat'
    status: HeartbeatStatus = field(default_factory=HeartbeatStatus)
    interval: int = 0         # 心跳间隔时间(ms)

@dataclass
class LifeCycleEvent(MetaEvent):
    """生命周期事件，用于通知框架生命周期变化"""
    meta_event_type: str = 'lifecycle'
    sub_type: LifeCycleSubType = LifeCycleSubType.ENABLE  # 子类型: enable, disable, connect
```

### 事件工厂：EventFactory

事件工厂是框架的核心组件之一，负责将原始 JSON 数据转换为强类型的事件对象：

```python
class EventFactory:
    @staticmethod
    def create_event(data: Dict[str, Any]) -> OneBotEvent:
        """根据数据创建事件对象"""
        post_type = data.get("post_type")
        
        if post_type == EventType.MESSAGE or post_type == EventType.MESSAGE_SENT:
            return EventFactory._create_message_event(data, common_args)
        elif post_type == EventType.NOTICE:
            return EventFactory._create_notice_event(data, common_args)
        elif post_type == EventType.REQUEST:
            return EventFactory._create_request_event(data, common_args)
        elif post_type == EventType.META:
            return EventFactory._create_meta_event(data, common_args)
        else:
            raise ValueError(f"Unknown event type: {post_type}")
```

### 在插件中使用事件

插件可以直接使用这些事件类型来处理各种场景：

```python
from core.command_manager import matcher
from core.bot import Bot
from models import GroupMessageEvent, PrivateMessageEvent
from models.events.notice import GroupIncreaseNoticeEvent
from models.events.request import FriendRequestEvent

# 处理群消息事件
@matcher.command("hello")
async def handle_hello(bot: Bot, event: GroupMessageEvent, args: list[str]):
    await event.reply(f"你好 {event.sender.nickname}！")

# 处理私聊消息事件
@matcher.command("help", permission_level=MessageEvent.USER)
async def handle_help(bot: Bot, event: PrivateMessageEvent, args: list[str]):
    await event.reply("这里是帮助信息...")

# 处理群成员增加通知
@matcher.on_notice("group_increase")
async def handle_group_increase(bot: Bot, event: GroupIncreaseNoticeEvent):
    await bot.send_group_msg(
        event.group_id, 
        f"欢迎新成员 {event.user_id} 加入！操作者：{event.operator_id}"
    )

# 处理加好友请求
@matcher.on_request("friend")
async def handle_friend_request(bot: Bot, event: FriendRequestEvent):
    # 自动同意所有好友请求
    await bot.set_friend_add_request(flag=event.flag, approve=True)
    await bot.send_private_msg(event.user_id, "已通过您的好友请求！")
```

### 事件处理的优势

1. **类型安全**：所有事件都有明确的类型定义，IDE 可以提供完整的代码提示和补全
2. **易于测试**：事件对象可以轻松构造，便于编写单元测试
3. **数据完整**：所有字段都有类型注解，确保数据的一致性和完整性
4. **性能优化**：使用 `@dataclass(slots=True)` 减少内存占用，提高属性访问速度
5. **可扩展性**：可以轻松定义自定义事件类型，扩展框架功能

### 常用事件属性速查

| 事件类型 | 关键属性 | 描述 |
|---------|---------|------|
| **MessageEvent** | `message_type`, `user_id`, `message`, `sender` | 所有消息事件的基类 |
| **PrivateMessageEvent** | 继承自 MessageEvent | 私聊消息事件 |
| **GroupMessageEvent** | `group_id`, `anonymous` | 群聊消息事件，包含群号和匿名信息 |
| **GroupIncreaseNoticeEvent** | `group_id`, `user_id`, `operator_id`, `sub_type` | 群成员增加通知 |
| **RecallGroupNoticeEvent** | `group_id`, `user_id`, `operator_id`, `message_id` | 群消息撤回通知 |
| **FriendRequestEvent** | `user_id`, `comment`, `flag` | 加好友请求事件 |
| **GroupRequestEvent** | `group_id`, `user_id`, `sub_type`, `comment`, `flag` | 加群请求/邀请事件 |
| **HeartbeatEvent** | `status`, `interval` | 心跳事件，用于监控连接状态 |

通过这套完整的事件模型，NEO 框架为开发者提供了强大而灵活的事件处理能力，同时保持了代码的类型安全和良好的开发体验。
