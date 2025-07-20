# 外观模式 (Facade Pattern)

外观模式是一种结构型设计模式，它为复杂的子系统提供一个简化的统一接口。通过外观模式，客户端可以通过一个简单的接口来访问复杂的子系统功能，而无需了解子系统的内部实现细节。

## 🎯 模式概述

外观模式的核心思想是"简化复杂性"。它通过创建一个外观类来封装子系统的复杂性，为客户端提供一个更简单、更易用的接口。

### 核心思想
- **简化接口**: 将复杂的子系统操作封装成简单的方法调用
- **降低耦合**: 客户端只需要与外观类交互，不直接依赖子系统
- **提高可维护性**: 子系统的变化不会影响客户端代码
- **更好的分层**: 为子系统定义清晰的访问层次

## 📁 文件列表

### 01_basic_facade.py
- **目的**: 外观模式的基础实现
- **内容**:
  - 智能家居控制系统示例
  - 展示外观模式的基本结构和使用
- **学习要点**:
  - 外观模式的核心概念
  - 如何整合多个子系统
  - 场景化操作的设计思路

### 02_media_facade.py
- **目的**: 媒体播放器外观示例
- **内容**:
  - 音频、视频、字幕处理子系统
  - 统一的媒体播放器外观
  - 不同播放模式的实现
- **学习要点**:
  - 多媒体系统的架构设计
  - 复杂操作的简化封装
  - 状态管理和错误处理

### 03_shopping_facade.py
- **目的**: 在线购物系统外观
- **内容**:
  - 用户、商品、订单、支付子系统
  - 统一的购物流程外观
  - 业务流程的封装
- **学习要点**:
  - 业务流程的协调
  - 事务处理的管理
  - 微服务架构中的外观应用

### 04_database_facade.py
- **目的**: 数据库访问外观
- **内容**:
  - 连接管理、查询构建、结果处理子系统
  - 统一的数据库访问接口
  - ORM的基本实现
- **学习要点**:
  - 数据库操作的抽象
  - 连接池和事务管理
  - 查询构建器的设计

### 05_real_world_examples.py
- **目的**: 外观模式的实际应用示例
- **内容**:
  - API网关、日志系统、配置管理等实际场景
  - 展示外观模式在不同领域的应用
- **学习要点**:
  - 外观模式的实际应用场景
  - 不同领域的设计技巧
  - 最佳实践和注意事项

## 🏗️ 模式结构

```
┌─────────────────┐    使用    ┌─────────────────┐
│     客户端      │ ────────→ │    外观类       │
│    (Client)     │           │   (Facade)      │
└─────────────────┘           └─────────────────┘
                                       │
                              协调和简化调用
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
            ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
            │  子系统A    │    │  子系统B    │    │  子系统C    │
            │(SubsystemA) │    │(SubsystemB) │    │(SubsystemC) │
            └─────────────┘    └─────────────┘    └─────────────┘
```

## 🎭 主要角色

- **客户端 (Client)**: 使用外观接口的代码，不直接与子系统交互
- **外观 (Facade)**: 提供简化的统一接口，协调各个子系统的工作
- **子系统 (Subsystems)**: 实现具体功能的独立模块，彼此可能相互依赖

## ✅ 模式优点

1. **简化复杂性**: 将复杂的子系统操作封装成简单的接口
2. **降低耦合度**: 客户端与子系统之间的依赖关系被最小化
3. **提高可维护性**: 子系统的变化不会直接影响客户端
4. **更好的分层**: 为系统提供清晰的层次结构
5. **易于使用**: 隐藏实现细节，提供直观的操作方式

## ❌ 模式缺点

1. **可能违反开闭原则**: 添加新子系统时可能需要修改外观类
2. **可能成为"上帝对象"**: 外观类承担过多责任时会变得复杂
3. **隐藏过多细节**: 可能限制高级用户对子系统的直接访问

## 🎯 适用场景

- **复杂系统简化**: 当子系统很复杂，需要提供简单接口时
- **分层架构**: 构建分层系统时，每层都可以有自己的外观
- **遗留系统集成**: 为老旧系统提供现代化的接口
- **第三方库封装**: 简化复杂第三方库的使用
- **微服务网关**: 为多个微服务提供统一的访问入口

## 💡 实现示例

### 基本外观模式实现

<augment_code_snippet path="16. Facade/01_basic_facade.py" mode="EXCERPT">
````python
class SmartHomeFacade:
    """智能家居外观类"""

    def __init__(self):
        # 初始化所有子系统
        self.lighting = LightingSystem()
        self.air_conditioning = AirConditioningSystem()
        self.audio = AudioSystem()
        self.security = SecuritySystem()

    def arrive_home_mode(self):
        """回家模式：开启基本照明和空调，解锁门禁"""
        print("🏠 启动回家模式...")
        actions = [
            self.security.disarm_system(),
            self.security.unlock_doors(),
            self.lighting.turn_on_light("客厅", 70),
            self.lighting.turn_on_light("厨房", 60),
            self.air_conditioning.turn_on_ac("客厅", 24, "制冷"),
            self.audio.turn_on(),
            self.audio.set_volume(30),
            self.audio.play_music("轻松音乐")
        ]

        for action in actions:
            print(f"  ✓ {action}")

        print("🎉 回家模式设置完成！欢迎回家！")
````
</augment_code_snippet>

### 媒体播放器外观示例

<augment_code_snippet path="16. Facade/02_media_facade.py" mode="EXCERPT">
````python
class MediaPlayerFacade:
    """媒体播放器外观类"""

    def __init__(self):
        # 初始化所有子系统
        self.audio_processor = AudioProcessor()
        self.video_processor = VideoProcessor()
        self.subtitle_processor = SubtitleProcessor()
        self.playback_controller = PlaybackController()
        self.current_media_type = None

    def play_video(self, file_path: str, format: VideoFormat = VideoFormat.MP4,
                   subtitle_path: Optional[str] = None):
        """播放视频文件（可选字幕）"""
        print(f"🎬 准备播放视频文件: {file_path}")

        actions = [
            self.video_processor.load_video(file_path, format),
            self.audio_processor.load_audio(file_path, AudioFormat.MP3),
            self.video_processor.start_playback(),
            self.audio_processor.start_playback(),
            self.playback_controller.play()
        ]

        # 如果有字幕文件，加载并启用字幕
        if subtitle_path:
            actions.extend([
                self.subtitle_processor.load_subtitle(subtitle_path),
                self.subtitle_processor.enable_subtitle()
            ])

        for action in actions:
            print(f"  ✓ {action}")

        self.current_media_type = MediaType.VIDEO
        print("🎥 视频播放已开始！")
````
</augment_code_snippet>

### API网关外观示例

<augment_code_snippet path="16. Facade/05_real_world_examples.py" mode="EXCERPT">
````python
class APIGatewayFacade:
    """API网关外观"""

    def __init__(self):
        self.auth_service = AuthenticationService()
        self.rate_limiting = RateLimitingService()
        self.logging = LoggingService()
        self.services = {
            "user": BackendService("用户服务"),
            "order": BackendService("订单服务"),
            "product": BackendService("商品服务")
        }

    def handle_request(self, token: str, service_name: str, endpoint: str,
                      method: str = "GET", data: Dict = None):
        """处理API请求"""
        print(f"🌐 API网关处理请求: {method} /{service_name}{endpoint}")

        # 1. 认证
        auth_result = self.auth_service.validate_token(token)
        print(f"  ✓ {auth_result}")

        # 2. 限流检查
        if not self.rate_limiting.check_rate_limit(user_id):
            return {"error": "请求频率过高", "code": 429}

        # 3. 记录日志
        log_msg = self.logging.log_request(user_id, endpoint, method)
        print(f"  ✓ {log_msg}")

        # 4. 路由到后端服务
        if service_name in self.services:
            service = self.services[service_name]
            result = service.process_request(data or {})
            return result
````
</augment_code_snippet>

## 🚀 运行方法

```bash
# 运行基础外观模式示例
python 01_basic_facade.py

# 运行媒体播放器外观示例
python 02_media_facade.py

# 运行在线购物外观示例
python 03_shopping_facade.py

# 运行数据库访问外观示例
python 04_database_facade.py

# 运行实际应用示例
python 05_real_world_examples.py
```

## 📚 学习建议

1. **理解简化思想**: 深入理解如何简化复杂系统的接口
2. **子系统协调**: 掌握如何协调多个子系统的工作
3. **接口设计**: 学会设计易用的高层接口
4. **实际应用**: 思考在API设计、系统集成中的应用
5. **避免过度设计**: 注意不要让外观类变得过于复杂

## 🌍 实际应用场景

- **API网关**: 为微服务提供统一入口
- **数据库访问层**: 简化复杂的数据库操作
- **第三方库封装**: 简化复杂库的使用
- **系统集成**: 整合多个子系统的功能
- **遗留系统**: 为老系统提供现代化接口

## 🔗 与其他模式的关系

- **适配器模式**: 都简化接口，但适配器主要解决兼容性问题
- **中介者模式**: 都减少对象间的耦合，但中介者关注对象间通信
- **抽象工厂模式**: 外观可以使用抽象工厂创建子系统对象
- **单例模式**: 外观类通常设计为单例

## ⚠️ 注意事项

1. **避免上帝对象**: 不要让外观类承担过多责任
2. **保持简单**: 外观接口应该简单易用
3. **不要隐藏所有功能**: 仍然允许客户端直接访问子系统
4. **版本兼容**: 考虑外观接口的向后兼容性

## 📋 前置知识

- 面向对象编程基础
- 系统设计的基本概念
- 接口设计原则
- 软件架构的基础知识

## 📖 后续学习

- 17. Flyweight（享元模式）
- 18. Proxy（代理模式）
- 行为型设计模式的学习

### 数据库访问外观示例
```python
import sqlite3
from typing import List, Dict, Any

# 数据库连接子系统
class DatabaseConnection:
    """数据库连接管理"""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """连接数据库"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return "数据库连接已建立"

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
        return "数据库连接已断开"

    def get_connection(self):
        """获取数据库连接"""
        if not self.connection:
            self.connect()
        return self.connection

# 查询构建子系统
class QueryBuilder:
    """SQL查询构建器"""
    def __init__(self):
        self.reset()

    def reset(self):
        """重置查询构建器"""
        self._select = []
        self._from = ""
        self._where = []
        self._order_by = []
        self._limit = None

    def select(self, columns: List[str]):
        """设置SELECT子句"""
        self._select = columns
        return self

    def from_table(self, table: str):
        """设置FROM子句"""
        self._from = table
        return self

    def where(self, condition: str):
        """添加WHERE条件"""
        self._where.append(condition)
        return self

    def order_by(self, column: str, direction: str = "ASC"):
        """添加ORDER BY子句"""
        self._order_by.append(f"{column} {direction}")
        return self

    def limit(self, count: int):
        """设置LIMIT子句"""
        self._limit = count
        return self

    def build(self) -> str:
        """构建SQL查询"""
        if not self._select or not self._from:
            raise ValueError("SELECT和FROM子句是必需的")

        query_parts = []
        query_parts.append(f"SELECT {', '.join(self._select)}")
        query_parts.append(f"FROM {self._from}")

        if self._where:
            query_parts.append(f"WHERE {' AND '.join(self._where)}")

        if self._order_by:
            query_parts.append(f"ORDER BY {', '.join(self._order_by)}")

        if self._limit:
            query_parts.append(f"LIMIT {self._limit}")

        return " ".join(query_parts)

# 结果处理子系统
class ResultProcessor:
    """查询结果处理器"""
    @staticmethod
    def to_dict_list(cursor) -> List[Dict[str, Any]]:
        """将查询结果转换为字典列表"""
        return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def to_single_dict(cursor) -> Dict[str, Any]:
        """将查询结果转换为单个字典"""
        row = cursor.fetchone()
        return dict(row) if row else {}

    @staticmethod
    def to_value_list(cursor, column: str) -> List[Any]:
        """提取指定列的值列表"""
        return [row[column] for row in cursor.fetchall()]

# 数据库外观
class DatabaseFacade:
    """数据库访问外观"""
    def __init__(self, db_path: str):
        self.db_connection = DatabaseConnection(db_path)
        self.query_builder = QueryBuilder()
        self.result_processor = ResultProcessor()

    def find_all(self, table: str, columns: List[str] = None) -> List[Dict[str, Any]]:
        """查找所有记录"""
        if columns is None:
            columns = ["*"]

        query = (self.query_builder
                .reset()
                .select(columns)
                .from_table(table)
                .build())

        return self._execute_query(query)

    def find_by_id(self, table: str, id_value: Any, id_column: str = "id") -> Dict[str, Any]:
        """根据ID查找记录"""
        query = (self.query_builder
                .reset()
                .select(["*"])
                .from_table(table)
                .where(f"{id_column} = ?")
                .build())

        conn = self.db_connection.get_connection()
        cursor = conn.execute(query, (id_value,))
        return self.result_processor.to_single_dict(cursor)

    def find_where(self, table: str, conditions: Dict[str, Any],
                   columns: List[str] = None, limit: int = None) -> List[Dict[str, Any]]:
        """根据条件查找记录"""
        if columns is None:
            columns = ["*"]

        builder = (self.query_builder
                  .reset()
                  .select(columns)
                  .from_table(table))

        # 添加WHERE条件
        where_conditions = []
        values = []
        for column, value in conditions.items():
            where_conditions.append(f"{column} = ?")
            values.append(value)

        for condition in where_conditions:
            builder.where(condition)

        if limit:
            builder.limit(limit)

        query = builder.build()

        conn = self.db_connection.get_connection()
        cursor = conn.execute(query, values)
        return self.result_processor.to_dict_list(cursor)

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """插入记录"""
        columns = list(data.keys())
        placeholders = ["?" for _ in columns]
        values = list(data.values())

        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"

        conn = self.db_connection.get_connection()
        cursor = conn.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    def update(self, table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> int:
        """更新记录"""
        set_clauses = [f"{column} = ?" for column in data.keys()]
        where_clauses = [f"{column} = ?" for column in conditions.keys()]

        query = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"

        values = list(data.values()) + list(conditions.values())

        conn = self.db_connection.get_connection()
        cursor = conn.execute(query, values)
        conn.commit()
        return cursor.rowcount

    def delete(self, table: str, conditions: Dict[str, Any]) -> int:
        """删除记录"""
        where_clauses = [f"{column} = ?" for column in conditions.keys()]
        query = f"DELETE FROM {table} WHERE {' AND '.join(where_clauses)}"

        values = list(conditions.values())

        conn = self.db_connection.get_connection()
        cursor = conn.execute(query, values)
        conn.commit()
        return cursor.rowcount

    def _execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询并返回结果"""
        conn = self.db_connection.get_connection()
        cursor = conn.execute(query, params)
        return self.result_processor.to_dict_list(cursor)

    def close(self):
        """关闭数据库连接"""
        self.db_connection.disconnect()

# 使用示例
def demo_database_facade():
    """数据库外观模式演示"""
    # 创建数据库外观
    db = DatabaseFacade(":memory:")  # 使用内存数据库

    # 创建测试表
    conn = db.db_connection.get_connection()
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            age INTEGER
        )
    """)
    conn.commit()

    print("=== 插入数据 ===")
    user_id1 = db.insert("users", {"name": "张三", "email": "zhangsan@example.com", "age": 25})
    user_id2 = db.insert("users", {"name": "李四", "email": "lisi@example.com", "age": 30})
    user_id3 = db.insert("users", {"name": "王五", "email": "wangwu@example.com", "age": 28})

    print(f"插入用户，ID: {user_id1}, {user_id2}, {user_id3}")

    print("\n=== 查找所有用户 ===")
    all_users = db.find_all("users")
    for user in all_users:
        print(f"ID: {user['id']}, 姓名: {user['name']}, 邮箱: {user['email']}, 年龄: {user['age']}")

    print("\n=== 根据ID查找用户 ===")
    user = db.find_by_id("users", user_id2)
    print(f"找到用户: {user}")

    print("\n=== 根据条件查找用户 ===")
    young_users = db.find_where("users", {"age": 25})
    print(f"25岁的用户: {young_users}")

    print("\n=== 更新用户 ===")
    updated_rows = db.update("users", {"age": 26}, {"id": user_id1})
    print(f"更新了 {updated_rows} 行")

    print("\n=== 删除用户 ===")
    deleted_rows = db.delete("users", {"id": user_id3})
    print(f"删除了 {deleted_rows} 行")

    print("\n=== 最终用户列表 ===")
    final_users = db.find_all("users")
    for user in final_users:
        print(f"ID: {user['id']}, 姓名: {user['name']}, 邮箱: {user['email']}, 年龄: {user['age']}")

    # 关闭数据库连接
    db.close()
```

## 运行方法

```bash
python "GroceryDisplay.py"
python "GroceryDispLite.py"
python "dbtest.py"
python "makesqllite.py"
```

## 学习建议

1. **理解简化思想**: 深入理解如何简化复杂系统的接口
2. **子系统协调**: 掌握如何协调多个子系统的工作
3. **接口设计**: 学会设计易用的高层接口
4. **实际应用**: 思考在API设计、系统集成中的应用
5. **避免过度设计**: 注意不要让外观类变得过于复杂

## 实际应用场景

- **API网关**: 为微服务提供统一入口
- **数据库访问层**: 简化复杂的数据库操作
- **第三方库封装**: 简化复杂库的使用
- **系统集成**: 整合多个子系统的功能
- **遗留系统**: 为老系统提供现代化接口

## 与其他模式的关系

- **适配器模式**: 都简化接口，但适配器主要解决兼容性问题
- **中介者模式**: 都减少对象间的耦合，但中介者关注对象间通信
- **抽象工厂模式**: 外观可以使用抽象工厂创建子系统对象
- **单例模式**: 外观类通常设计为单例

## 注意事项

1. **避免上帝对象**: 不要让外观类承担过多责任
2. **保持简单**: 外观接口应该简单易用
3. **不要隐藏所有功能**: 仍然允许客户端直接访问子系统
4. **版本兼容**: 考虑外观接口的向后兼容性

## 前置知识

- 面向对象编程基础
- 系统设计的基本概念
- 接口设计原则
- 软件架构的基础知识

## 后续学习

- 17. Flyweight（享元模式）
- 18. Proxy（代理模式）
- 行为型设计模式的学习
