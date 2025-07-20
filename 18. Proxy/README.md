# 代理模式 (Proxy Pattern)

代理模式是一种结构型设计模式，它为其他对象提供一种代理以控制对这个对象的访问。代理对象与目标对象实现相同的接口，可以在访问目标对象前后添加额外的处理逻辑，如权限控制、缓存、延迟加载等。

## 🎯 模式概述

代理模式的核心思想是"控制访问"。通过引入一个代理对象来间接访问目标对象，代理可以在不改变目标对象的情况下，增加额外的功能或控制访问行为。

### 核心思想
- **访问控制**: 控制对目标对象的访问权限
- **延迟加载**: 在真正需要时才创建目标对象
- **缓存机制**: 缓存昂贵操作的结果
- **透明性**: 对客户端来说，代理和真实对象是透明的

## 📁 文件列表

### 01_basic_proxy.py
- **目的**: 代理模式的基础实现
- **内容**:
  - 基本的代理接口和实现
  - 虚拟代理的延迟加载
  - 代理的透明性演示
- **学习要点**:
  - 代理模式的核心概念
  - 代理接口的设计
  - 延迟加载的实现

### 02_protection_proxy.py
- **目的**: 保护代理示例
- **内容**:
  - 权限控制系统
  - 用户角色管理
  - 访问权限验证
- **学习要点**:
  - 保护代理的设计
  - 权限控制的实现
  - 安全访问机制

### 03_cache_proxy.py
- **目的**: 缓存代理示例
- **内容**:
  - 缓存机制的实现
  - 性能优化策略
  - 缓存失效处理
- **学习要点**:
  - 缓存代理的设计
  - 性能优化技术
  - 缓存策略的选择

### 04_remote_proxy.py
- **目的**: 远程代理示例
- **内容**:
  - 网络服务代理
  - API调用封装
  - 错误处理和重试机制
- **学习要点**:
  - 远程代理的实现
  - 网络通信的封装
  - 分布式系统的代理应用

### 05_real_world_examples.py
- **目的**: 代理模式的实际应用示例
- **内容**:
  - 数据库连接代理
  - 图片加载代理
  - 日志记录代理等实际场景
- **学习要点**:
  - 代理模式的实际应用场景
  - 不同领域的代理技巧
  - 最佳实践和注意事项

## 🏗️ 模式结构

```
┌─────────────────┐    使用    ┌─────────────────┐
│     客户端      │ ────────→ │    代理对象     │
│    (Client)     │           │    (Proxy)      │
└─────────────────┘           └─────────────────┘
                                       │
                                   委托调用
                                       │
                                       ▼
                              ┌─────────────────┐
                              │   真实对象      │
                              │ (RealSubject)   │
                              └─────────────────┘
                                       △
                                       │
                                   实现
                                       │
                              ┌─────────────────┐
                              │   抽象主题      │
                              │   (Subject)     │
                              └─────────────────┘
```

## 🎭 主要角色

- **抽象主题 (Subject)**: 定义代理和真实对象的公共接口
- **真实主题 (RealSubject)**: 实际执行业务逻辑的对象
- **代理 (Proxy)**: 控制对真实对象的访问，可以在访问前后添加额外处理
- **客户端 (Client)**: 通过代理访问真实对象，对代理和真实对象无感知

## 🔄 代理类型

### 虚拟代理 (Virtual Proxy)
- **目的**: 延迟创建昂贵的对象
- **应用**: 图片加载、大文件处理、数据库连接
- **优势**: 节省内存和初始化时间

### 保护代理 (Protection Proxy)
- **目的**: 控制对对象的访问权限
- **应用**: 权限验证、安全控制、访问日志
- **优势**: 增强安全性，集中权限管理

### 远程代理 (Remote Proxy)
- **目的**: 为远程对象提供本地代表
- **应用**: RPC调用、Web服务、分布式系统
- **优势**: 隐藏网络通信复杂性

### 缓存代理 (Cache Proxy)
- **目的**: 缓存昂贵操作的结果
- **应用**: 数据库查询、API调用、计算结果
- **优势**: 提高性能，减少重复计算

## ✅ 模式优点

1. **访问控制**: 可以控制对目标对象的访问
2. **延迟加载**: 在需要时才创建昂贵的对象
3. **缓存机制**: 可以缓存结果提高性能
4. **透明性**: 客户端无需知道是否使用了代理
5. **功能增强**: 在不修改原对象的情况下增加功能
6. **解耦合**: 将客户端与复杂的子系统解耦

## ❌ 模式缺点

1. **复杂性增加**: 增加了系统的复杂性
2. **性能开销**: 代理调用可能带来额外开销
3. **间接访问**: 增加了一层间接访问
4. **维护成本**: 需要维护代理和真实对象的一致性

## 🎯 适用场景

- **延迟加载**: 对象创建成本高，需要延迟初始化
- **访问控制**: 需要控制对对象的访问权限
- **远程访问**: 需要访问远程对象或服务
- **缓存需求**: 需要缓存昂贵操作的结果
- **日志记录**: 需要记录对象的访问日志
- **性能监控**: 需要监控对象的使用情况

## 💡 实现示例

### 基本代理模式实现

<augment_code_snippet path="18. Proxy/01_basic_proxy.py" mode="EXCERPT">
````python
class VirtualProxy(Subject):
    """虚拟代理 - 延迟创建真实对象"""

    def __init__(self, name: str):
        self.name = name
        self._real_subject: Optional[RealSubject] = None
        print(f"创建虚拟代理: {name}")

    def request(self) -> str:
        # 延迟创建真实对象
        if self._real_subject is None:
            print(f"代理: 首次访问，创建真实对象")
            self._real_subject = RealSubject(self.name)

        # 委托给真实对象
        return self._real_subject.request()
````
</augment_code_snippet>

### 保护代理示例

<augment_code_snippet path="18. Proxy/02_protection_proxy.py" mode="EXCERPT">
````python
class DatabaseProtectionProxy(SensitiveResource):
    """数据库保护代理"""

    def __init__(self, database: DatabaseResource):
        self._database = database
        self._current_session: Optional[Session] = None

    def read_data(self) -> str:
        if not self._check_permission(Permission.READ):
            return "访问被拒绝: 没有读取权限"

        return self._database.read_data()

    def _check_permission(self, required_permission: Permission) -> bool:
        if not self._current_session or not self._current_session.is_valid():
            return False
        return self._current_session.user.has_permission(required_permission)
````
</augment_code_snippet>

### 缓存代理示例

<augment_code_snippet path="18. Proxy/03_cache_proxy.py" mode="EXCERPT">
````python
class CacheProxy(DataService):
    """缓存代理"""

    def __init__(self, data_service: DataService, cache_manager: CacheManager):
        self.data_service = data_service
        self.cache_manager = cache_manager

    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        cache_key = f"user_data:{user_id}"

        # 尝试从缓存获取
        cached_data = self.cache_manager.get(cache_key)
        if cached_data is not None:
            return cached_data

        # 缓存未命中，从真实服务获取
        data = self.data_service.get_user_data(user_id)
        self.cache_manager.put(cache_key, data, ttl_seconds=600)
        return data
````
</augment_code_snippet>

## 🚀 运行方法

```bash
# 运行基础代理模式示例
python 01_basic_proxy.py

# 运行保护代理示例
python 02_protection_proxy.py

# 运行缓存代理示例
python 03_cache_proxy.py

# 运行远程代理示例
python 04_remote_proxy.py

# 运行实际应用示例
python 05_real_world_examples.py
```

## 📚 学习建议

1. **理解代理类型**: 掌握不同类型代理的应用场景
2. **透明性设计**: 确保代理对客户端是透明的
3. **性能考虑**: 平衡代理带来的好处和开销
4. **错误处理**: 正确处理代理中的异常情况
5. **线程安全**: 在多线程环境中确保代理的安全性

## 🌍 实际应用场景

- **ORM框架**: 数据库对象的延迟加载
- **Web框架**: HTTP请求的代理和缓存
- **图片加载**: 大图片的延迟加载和缓存
- **权限系统**: 基于角色的访问控制
- **分布式系统**: 远程服务的本地代理
- **性能监控**: 方法调用的监控和统计

## 🔗 与其他模式的关系

- **装饰器模式**: 都为对象添加功能，但代理控制访问，装饰器增强功能
- **适配器模式**: 都提供不同接口，但代理保持接口一致，适配器转换接口
- **外观模式**: 都简化访问，但代理控制单个对象，外观简化子系统
- **享元模式**: 代理可以管理享元对象的创建和访问

## ⚠️ 注意事项

1. **接口一致性**: 确保代理和真实对象实现相同接口
2. **生命周期管理**: 正确管理真实对象的生命周期
3. **异常传播**: 正确传播真实对象抛出的异常
4. **内存泄漏**: 避免代理持有不必要的引用
5. **性能监控**: 监控代理带来的性能影响

## 📋 前置知识

- 面向对象编程基础
- 接口和抽象类的使用
- 设计模式基本概念
- 多线程编程基础

## 📖 后续学习

- 行为型设计模式的学习
- 分布式系统设计
- 缓存策略和实现
- 权限控制系统设计

## 模式结构

```
Subject (抽象主题)
    └── request(): void

RealSubject (真实主题)
    └── request(): void

Proxy (代理)
    ├── realSubject: RealSubject
    ├── request(): void
    ├── preRequest(): void
    └── postRequest(): void

Client (客户端)
    └── 通过Proxy访问RealSubject
```

## 主要角色

- **Subject（抽象主题）**: 定义RealSubject和Proxy的共用接口
- **RealSubject（真实主题）**: 定义Proxy所代表的真实实体
- **Proxy（代理）**: 保存一个引用使得代理可以访问实体，控制对RealSubject的访问

## 代理类型

### 1. 虚拟代理（Virtual Proxy）
延迟创建开销大的对象，直到真正需要时才创建。

### 2. 保护代理（Protection Proxy）
控制对原始对象的访问，提供权限验证。

### 3. 缓存代理（Cache Proxy）
为开销大的运算结果提供暂时存储。

### 4. 远程代理（Remote Proxy）
为位于不同地址空间的对象提供本地代表。

### 5. 智能引用代理（Smart Reference Proxy）
在访问对象时执行额外的操作，如引用计数、线程安全检查等。

## 模式优点

1. **职责清晰**: 代理对象和真实对象职责明确
2. **高扩展性**: 可以在不修改真实对象的情况下扩展功能
3. **智能化**: 可以根据需要创建对象，提高性能
4. **保护性**: 可以控制对真实对象的访问

## 模式缺点

1. **增加复杂性**: 增加了系统的复杂度
2. **性能开销**: 代理对象可能增加请求的处理时间

## 使用场景

- 需要在访问对象时进行额外的控制
- 需要延迟对象的创建和初始化
- 需要为网络上的对象提供本地代表
- 需要对对象的访问进行权限控制

## 实现示例

### 基本代理模式实现
```python
from abc import ABC, abstractmethod
import time

# 抽象主题
class Subject(ABC):
    """抽象主题接口"""
    @abstractmethod
    def request(self):
        pass

# 真实主题
class RealSubject(Subject):
    """真实主题"""
    def __init__(self, name: str):
        self.name = name
        print(f"创建真实对象: {self.name}")

    def request(self):
        """处理请求"""
        print(f"真实对象 {self.name} 处理请求")
        time.sleep(1)  # 模拟耗时操作
        return f"真实对象 {self.name} 的响应"

# 代理
class Proxy(Subject):
    """代理类"""
    def __init__(self, name: str):
        self.name = name
        self._real_subject = None

    def request(self):
        """代理请求"""
        # 前置处理
        self._pre_request()

        # 延迟创建真实对象
        if self._real_subject is None:
            self._real_subject = RealSubject(self.name)

        # 委托给真实对象
        result = self._real_subject.request()

        # 后置处理
        self._post_request()

        return result

    def _pre_request(self):
        """请求前处理"""
        print(f"代理 {self.name}: 请求前处理")

    def _post_request(self):
        """请求后处理"""
        print(f"代理 {self.name}: 请求后处理")

# 使用示例
def demo_basic_proxy():
    """基本代理模式演示"""
    print("=== 创建代理对象 ===")
    proxy = Proxy("测试对象")

    print("\n=== 第一次请求 ===")
    result1 = proxy.request()
    print(f"结果: {result1}")

    print("\n=== 第二次请求 ===")
    result2 = proxy.request()
    print(f"结果: {result2}")
```

### 虚拟代理示例
```python
import time
from typing import Optional

# 大型图片类
class LargeImage:
    """大型图片类（真实主题）"""
    def __init__(self, filename: str):
        self.filename = filename
        self._load_image()

    def _load_image(self):
        """加载图片（模拟耗时操作）"""
        print(f"正在加载大型图片: {self.filename}")
        time.sleep(2)  # 模拟加载时间
        print(f"图片 {self.filename} 加载完成")

    def display(self):
        """显示图片"""
        print(f"显示图片: {self.filename}")

    def get_size(self):
        """获取图片大小"""
        return f"{self.filename} 大小: 1920x1080"

# 图片接口
class Image(ABC):
    """图片接口"""
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def get_size(self):
        pass

# 图片虚拟代理
class ImageProxy(Image):
    """图片虚拟代理"""
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image: Optional[LargeImage] = None

    def display(self):
        """显示图片"""
        if self._real_image is None:
            print(f"首次访问，创建真实图片对象")
            self._real_image = LargeImage(self.filename)

        self._real_image.display()

    def get_size(self):
        """获取图片大小（不需要加载真实图片）"""
        # 可以从文件头或缓存中获取大小信息
        return f"{self.filename} 大小: 1920x1080 (来自代理缓存)"

# 图片查看器
class ImageViewer:
    """图片查看器"""
    def __init__(self):
        self.images = []

    def add_image(self, image: Image):
        """添加图片"""
        self.images.append(image)
        print(f"添加图片到查看器")

    def show_image_info(self):
        """显示图片信息"""
        print("\n=== 图片信息 ===")
        for i, image in enumerate(self.images, 1):
            print(f"{i}. {image.get_size()}")

    def display_image(self, index: int):
        """显示指定图片"""
        if 0 <= index < len(self.images):
            print(f"\n=== 显示第 {index + 1} 张图片 ===")
            self.images[index].display()

# 使用示例
def demo_virtual_proxy():
    """虚拟代理演示"""
    viewer = ImageViewer()

    print("=== 添加图片到查看器 ===")
    # 使用代理，图片不会立即加载
    viewer.add_image(ImageProxy("photo1.jpg"))
    viewer.add_image(ImageProxy("photo2.jpg"))
    viewer.add_image(ImageProxy("photo3.jpg"))

    # 查看图片信息，不会触发图片加载
    viewer.show_image_info()

    # 只有在真正显示时才加载图片
    viewer.display_image(0)
    viewer.display_image(1)
```

### 保护代理示例
```python
from enum import Enum

class UserRole(Enum):
    """用户角色"""
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"

class User:
    """用户类"""
    def __init__(self, username: str, role: UserRole):
        self.username = username
        self.role = role

# 敏感文档类
class SensitiveDocument:
    """敏感文档（真实主题）"""
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def read(self):
        """读取文档"""
        return f"文档标题: {self.title}\n内容: {self.content}"

    def write(self, content: str):
        """写入文档"""
        self.content = content
        return f"文档已更新: {self.title}"

    def delete(self):
        """删除文档"""
        return f"文档已删除: {self.title}"

# 文档接口
class Document(ABC):
    """文档接口"""
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, content: str):
        pass

    @abstractmethod
    def delete(self):
        pass

# 文档保护代理
class DocumentProtectionProxy(Document):
    """文档保护代理"""
    def __init__(self, document: SensitiveDocument, user: User):
        self._document = document
        self._user = user

    def read(self):
        """读取文档"""
        if self._check_read_permission():
            return self._document.read()
        else:
            return "访问被拒绝: 没有读取权限"

    def write(self, content: str):
        """写入文档"""
        if self._check_write_permission():
            return self._document.write(content)
        else:
            return "访问被拒绝: 没有写入权限"

    def delete(self):
        """删除文档"""
        if self._check_delete_permission():
            return self._document.delete()
        else:
            return "访问被拒绝: 没有删除权限"

    def _check_read_permission(self) -> bool:
        """检查读取权限"""
        # 所有用户都可以读取
        return self._user.role in [UserRole.USER, UserRole.ADMIN]

    def _check_write_permission(self) -> bool:
        """检查写入权限"""
        # 只有用户和管理员可以写入
        return self._user.role in [UserRole.USER, UserRole.ADMIN]

    def _check_delete_permission(self) -> bool:
        """检查删除权限"""
        # 只有管理员可以删除
        return self._user.role == UserRole.ADMIN

# 使用示例
def demo_protection_proxy():
    """保护代理演示"""
    # 创建敏感文档
    document = SensitiveDocument("机密报告", "这是一份机密文档的内容")

    # 创建不同角色的用户
    guest = User("访客", UserRole.GUEST)
    user = User("普通用户", UserRole.USER)
    admin = User("管理员", UserRole.ADMIN)

    users = [guest, user, admin]

    for current_user in users:
        print(f"\n=== {current_user.username} ({current_user.role.value}) 的操作 ===")

        # 创建保护代理
        proxy = DocumentProtectionProxy(document, current_user)

        # 尝试各种操作
        print("读取:", proxy.read())
        print("写入:", proxy.write("更新的内容"))
        print("删除:", proxy.delete())
```

### 缓存代理示例
```python
import time
import hashlib
from typing import Dict, Any

# 数据库服务
class DatabaseService:
    """数据库服务（真实主题）"""
    def __init__(self):
        self.query_count = 0

    def query(self, sql: str) -> str:
        """执行数据库查询"""
        self.query_count += 1
        print(f"执行数据库查询 #{self.query_count}: {sql}")

        # 模拟数据库查询延迟
        time.sleep(1)

        # 模拟查询结果
        if "users" in sql.lower():
            return f"用户数据结果 (查询: {sql})"
        elif "products" in sql.lower():
            return f"产品数据结果 (查询: {sql})"
        else:
            return f"通用查询结果 (查询: {sql})"

# 数据库接口
class Database(ABC):
    """数据库接口"""
    @abstractmethod
    def query(self, sql: str) -> str:
        pass

# 缓存代理
class CachingDatabaseProxy(Database):
    """缓存数据库代理"""
    def __init__(self, database: DatabaseService, cache_ttl: int = 300):
        self._database = database
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = cache_ttl  # 缓存生存时间（秒）

    def query(self, sql: str) -> str:
        """执行查询（带缓存）"""
        cache_key = self._generate_cache_key(sql)

        # 检查缓存
        if self._is_cache_valid(cache_key):
            print(f"缓存命中: {sql}")
            return self._cache[cache_key]['result']

        # 缓存未命中，执行真实查询
        print(f"缓存未命中，执行真实查询")
        result = self._database.query(sql)

        # 存储到缓存
        self._cache[cache_key] = {
            'result': result,
            'timestamp': time.time()
        }

        return result

    def _generate_cache_key(self, sql: str) -> str:
        """生成缓存键"""
        return hashlib.md5(sql.encode()).hexdigest()

    def _is_cache_valid(self, cache_key: str) -> bool:
        """检查缓存是否有效"""
        if cache_key not in self._cache:
            return False

        cache_time = self._cache[cache_key]['timestamp']
        return (time.time() - cache_time) < self._cache_ttl

    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        print("缓存已清空")

    def get_cache_stats(self):
        """获取缓存统计"""
        return {
            'cache_size': len(self._cache),
            'database_queries': self._database.query_count
        }

# 使用示例
def demo_caching_proxy():
    """缓存代理演示"""
    # 创建数据库服务和缓存代理
    db_service = DatabaseService()
    db_proxy = CachingDatabaseProxy(db_service, cache_ttl=5)  # 5秒缓存

    queries = [
        "SELECT * FROM users WHERE id = 1",
        "SELECT * FROM products WHERE category = 'electronics'",
        "SELECT * FROM users WHERE id = 1",  # 重复查询
        "SELECT * FROM orders WHERE date > '2023-01-01'"
    ]

    print("=== 执行查询 ===")
    for i, query in enumerate(queries, 1):
        print(f"\n--- 查询 {i} ---")
        result = db_proxy.query(query)
        print(f"结果: {result}")

        # 显示统计信息
        stats = db_proxy.get_cache_stats()
        print(f"缓存大小: {stats['cache_size']}, 数据库查询次数: {stats['database_queries']}")

    print("\n=== 重复执行相同查询 ===")
    # 再次执行第一个查询，应该命中缓存
    result = db_proxy.query(queries[0])
    print(f"结果: {result}")

    print("\n=== 等待缓存过期 ===")
    time.sleep(6)  # 等待缓存过期
    result = db_proxy.query(queries[0])
    print(f"结果: {result}")

    # 最终统计
    final_stats = db_proxy.get_cache_stats()
    print(f"\n最终统计 - 缓存大小: {final_stats['cache_size']}, 数据库查询次数: {final_stats['database_queries']}")
```

### 智能引用代理示例
```python
import threading
from typing import Set

# 共享资源
class SharedResource:
    """共享资源（真实主题）"""
    def __init__(self, name: str):
        self.name = name
        self.data = f"共享数据: {name}"

    def read_data(self) -> str:
        """读取数据"""
        return self.data

    def write_data(self, data: str):
        """写入数据"""
        self.data = data
        print(f"数据已更新: {data}")

# 资源接口
class Resource(ABC):
    """资源接口"""
    @abstractmethod
    def read_data(self) -> str:
        pass

    @abstractmethod
    def write_data(self, data: str):
        pass

# 智能引用代理
class SmartReferenceProxy(Resource):
    """智能引用代理"""
    def __init__(self, resource: SharedResource):
        self._resource = resource
        self._reference_count = 0
        self._lock = threading.Lock()
        self._clients: Set[str] = set()

    def read_data(self) -> str:
        """读取数据"""
        client_id = threading.current_thread().name

        with self._lock:
            self._reference_count += 1
            self._clients.add(client_id)
            print(f"客户端 {client_id} 开始读取，当前引用计数: {self._reference_count}")

        try:
            result = self._resource.read_data()
            return result
        finally:
            with self._lock:
                self._reference_count -= 1
                print(f"客户端 {client_id} 读取完成，当前引用计数: {self._reference_count}")

    def write_data(self, data: str):
        """写入数据"""
        client_id = threading.current_thread().name

        with self._lock:
            if self._reference_count > 1:
                print(f"警告: 客户端 {client_id} 尝试写入时有其他客户端正在访问")

            print(f"客户端 {client_id} 开始写入")
            self._resource.write_data(data)
            print(f"客户端 {client_id} 写入完成")

    def get_reference_count(self) -> int:
        """获取引用计数"""
        return self._reference_count

    def get_active_clients(self) -> Set[str]:
        """获取活跃客户端"""
        return self._clients.copy()

# 使用示例
def demo_smart_reference_proxy():
    """智能引用代理演示"""
    resource = SharedResource("重要数据")
    proxy = SmartReferenceProxy(resource)

    def client_operation(client_name: str, operation: str):
        """客户端操作"""
        threading.current_thread().name = client_name

        if operation == "read":
            data = proxy.read_data()
            print(f"{client_name} 读取到: {data}")
            time.sleep(1)  # 模拟处理时间
        elif operation == "write":
            proxy.write_data(f"来自 {client_name} 的数据")

    print("=== 智能引用代理演示 ===")

    # 创建多个线程模拟并发访问
    threads = []

    # 创建读取线程
    for i in range(3):
        thread = threading.Thread(
            target=client_operation,
            args=(f"读取客户端{i+1}", "read")
        )
        threads.append(thread)

    # 创建写入线程
    write_thread = threading.Thread(
        target=client_operation,
        args=("写入客户端", "write")
    )
    threads.append(write_thread)

    # 启动所有线程
    for thread in threads:
        thread.start()
        time.sleep(0.1)  # 稍微错开启动时间

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print(f"\n最终引用计数: {proxy.get_reference_count()}")
    print(f"活跃客户端: {proxy.get_active_clients()}")
```

## 运行方法

```bash
python "ProxyDemo.py"
```

## 学习建议

1. **理解代理类型**: 深入理解不同类型代理的应用场景
2. **透明性设计**: 掌握如何让代理对客户端透明
3. **性能权衡**: 理解代理模式的性能影响
4. **实际应用**: 思考在网络编程、缓存系统中的应用
5. **安全考虑**: 学会使用代理进行权限控制

## 实际应用场景

- **网络代理**: HTTP代理、反向代理
- **ORM框架**: 数据库对象的延迟加载
- **缓存系统**: Redis、Memcached的客户端
- **权限控制**: 访问控制和安全验证
- **远程调用**: RPC、Web服务的本地代理

## 与其他模式的关系

- **装饰器模式**: 都为对象添加功能，但代理控制访问
- **适配器模式**: 都作为中间层，但适配器改变接口
- **外观模式**: 都简化访问，但外观模式简化复杂子系统
- **享元模式**: 代理可以控制享元对象的访问

## 注意事项

1. **性能开销**: 代理会增加一定的性能开销
2. **复杂性**: 不要过度使用代理模式
3. **线程安全**: 多线程环境下的代理需要考虑线程安全
4. **内存管理**: 注意代理对象的生命周期管理

## 前置知识

- 面向对象编程基础
- 接口和抽象类的概念
- 多线程编程基础（可选）
- 网络编程基础（可选）

## 后续学习

- 行为型设计模式的学习
- 系统架构设计
- 性能优化技术
- 分布式系统设计
