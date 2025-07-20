# 策略模式 (Strategy Pattern)

策略模式是一种行为型设计模式，它定义了一系列算法，把它们一个个封装起来，并且使它们可相互替换。策略模式让算法的变化独立于使用算法的客户，使得算法可以在不影响客户端的情况下发生变化。

## 核心概念

策略模式的核心思想是：
- **算法封装**：将每个算法封装在独立的策略类中
- **可替换性**：不同策略可以相互替换而不影响客户端
- **运行时选择**：可以在运行时动态选择和切换算法
- **消除条件语句**：避免大量的if-else或switch语句

## 文件列表

### 01_basic_strategy.py
- **目的**: 策略模式的基础实现
- **内容**:
  - 抽象策略和上下文接口
  - 简单的策略实现示例
  - 策略的动态切换机制
- **学习要点**:
  - 理解策略模式的核心结构
  - 掌握策略接口的设计原则
  - 学习上下文与策略的关系

### 02_sorting_algorithms.py
- **目的**: 排序算法策略实现
- **内容**:
  - 多种排序算法的策略封装
  - 性能比较和算法选择
  - 大数据量的策略优化
- **学习要点**:
  - 算法策略的实际应用
  - 性能测试和比较方法
  - 根据数据特征选择策略

### 03_payment_system.py
- **目的**: 支付系统策略模式
- **内容**:
  - 多种支付方式的策略实现
  - 支付流程的统一处理
  - 支付策略的扩展机制
- **学习要点**:
  - 业务系统中的策略应用
  - 策略模式的扩展性设计
  - 实际项目中的最佳实践

### 04_data_processing.py
- **目的**: 数据处理策略系统
- **内容**:
  - 数据验证、转换、存储策略
  - 策略链和策略组合
  - 异步处理策略
- **学习要点**:
  - 复杂业务场景的策略设计
  - 策略的组合和链式调用
  - 异步策略的实现方式

### 05_real_world_examples.py
- **目的**: 实际项目中的策略模式应用
- **内容**:
  - 文件压缩策略系统
  - 图像处理策略
  - 缓存策略管理
- **学习要点**:
  - 策略模式在不同领域的应用
  - 策略工厂和策略注册机制
  - 性能优化和资源管理

## 模式结构

```
Context (上下文)
    ├── strategy: Strategy              # 当前策略对象
    ├── set_strategy(strategy): void    # 设置策略
    └── execute_algorithm(): void       # 执行算法
         └── strategy.algorithm()       # 委托给策略执行

Strategy (抽象策略)
    └── algorithm(): void               # 算法接口

ConcreteStrategyA (具体策略A)
    └── algorithm(): void               # 算法A的具体实现

ConcreteStrategyB (具体策略B)
    └── algorithm(): void               # 算法B的具体实现
```

## 主要角色

- **Context（上下文）**: 维护一个对策略对象的引用，定义客户端使用的接口
- **Strategy（抽象策略）**: 定义所有具体策略的公共接口
- **ConcreteStrategy（具体策略）**: 实现抽象策略接口，提供具体的算法实现

## 模式优点

1. **算法可替换**: 算法可以在运行时动态切换
2. **避免条件语句**: 消除大量的if-else或switch语句
3. **扩展性好**: 增加新算法只需要增加新的策略类
4. **符合开闭原则**: 对扩展开放，对修改关闭
5. **职责分离**: 算法的实现和使用分离

## 模式缺点

1. **客户端复杂**: 客户端必须了解所有策略的区别
2. **策略类增多**: 每个算法都需要一个策略类
3. **通信开销**: 策略和上下文之间可能需要传递大量数据

## 使用场景

- **多种算法**: 一个系统需要动态地在几种算法中选择一种
- **算法变化**: 算法经常变化或需要扩展新算法
- **条件语句复杂**: 有很多条件语句用于选择算法
- **算法封装**: 需要隐藏算法的实现细节
- **运行时选择**: 需要在运行时根据环境选择不同的算法

## 快速开始

### 基本使用示例

```python
from abc import ABC, abstractmethod

# 1. 定义策略接口
class Strategy(ABC):
    @abstractmethod
    def execute(self, data) -> any:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

# 2. 定义上下文类
class Context:
    def __init__(self, strategy: Strategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy
        print(f"切换策略: {strategy.get_name()}")

    def execute_strategy(self, data) -> any:
        if not self._strategy:
            raise ValueError("未设置策略")
        return self._strategy.execute(data)

# 3. 实现具体策略
class SortAscStrategy(Strategy):
    def execute(self, data) -> list:
        return sorted(data)

    def get_name(self) -> str:
        return "升序排序"

class SortDescStrategy(Strategy):
    def execute(self, data) -> list:
        return sorted(data, reverse=True)

    def get_name(self) -> str:
        return "降序排序"

class FilterEvenStrategy(Strategy):
    def execute(self, data) -> list:
        return [x for x in data if x % 2 == 0]

    def get_name(self) -> str:
        return "偶数过滤"

# 4. 使用示例
def main():
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    context = Context()

    # 测试不同策略
    strategies = [
        SortAscStrategy(),
        SortDescStrategy(),
        FilterEvenStrategy()
    ]

    for strategy in strategies:
        context.set_strategy(strategy)
        result = context.execute_strategy(data)
        print(f"结果: {result}")

if __name__ == "__main__":
    main()
```

### 排序策略示例
```python
import time
import random

# 排序策略接口
class SortStrategy(ABC):
    """排序策略接口"""
    @abstractmethod
    def sort(self, data):
        pass

    @abstractmethod
    def get_name(self):
        pass

# 冒泡排序策略
class BubbleSortStrategy(SortStrategy):
    """冒泡排序策略"""
    def sort(self, data):
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def get_name(self):
        return "冒泡排序"

# 快速排序策略
class QuickSortStrategy(SortStrategy):
    """快速排序策略"""
    def sort(self, data):
        arr = data.copy()
        self._quick_sort(arr, 0, len(arr) - 1)
        return arr

    def _quick_sort(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick_sort(arr, low, pi - 1)
            self._quick_sort(arr, pi + 1, high)

    def _partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def get_name(self):
        return "快速排序"

# 归并排序策略
class MergeSortStrategy(SortStrategy):
    """归并排序策略"""
    def sort(self, data):
        arr = data.copy()
        self._merge_sort(arr, 0, len(arr) - 1)
        return arr

    def _merge_sort(self, arr, left, right):
        if left < right:
            mid = (left + right) // 2
            self._merge_sort(arr, left, mid)
            self._merge_sort(arr, mid + 1, right)
            self._merge(arr, left, mid, right)

    def _merge(self, arr, left, mid, right):
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

    def get_name(self):
        return "归并排序"

# 内置排序策略
class PythonSortStrategy(SortStrategy):
    """Python内置排序策略"""
    def sort(self, data):
        return sorted(data)

    def get_name(self):
        return "Python内置排序"

# 排序上下文
class SortContext:
    """排序上下文"""
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        """设置排序策略"""
        self._strategy = strategy

    def sort_data(self, data):
        """排序数据"""
        start_time = time.time()
        result = self._strategy.sort(data)
        end_time = time.time()

        print(f"{self._strategy.get_name()}: {end_time - start_time:.6f}秒")
        return result

# 使用示例
def demo_sort_strategy():
    """排序策略演示"""
    # 生成测试数据
    small_data = [random.randint(1, 100) for _ in range(20)]
    large_data = [random.randint(1, 1000) for _ in range(1000)]

    # 创建策略
    strategies = [
        BubbleSortStrategy(),
        QuickSortStrategy(),
        MergeSortStrategy(),
        PythonSortStrategy()
    ]

    context = SortContext(strategies[0])

    print("=== 小数据集排序 (20个元素) ===")
    print(f"原始数据: {small_data[:10]}...")

    for strategy in strategies:
        context.set_strategy(strategy)
        sorted_data = context.sort_data(small_data)
        print(f"排序结果: {sorted_data[:10]}...")
        print()

    print("=== 大数据集排序 (1000个元素) ===")
    for strategy in strategies:
        context.set_strategy(strategy)
        context.sort_data(large_data)
```

### 支付策略示例
```python
# 支付策略接口
class PaymentStrategy(ABC):
    """支付策略接口"""
    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def get_payment_type(self):
        pass

# 信用卡支付策略
class CreditCardPayment(PaymentStrategy):
    """信用卡支付策略"""
    def __init__(self, card_number, holder_name, cvv):
        self.card_number = card_number
        self.holder_name = holder_name
        self.cvv = cvv

    def pay(self, amount):
        print(f"使用信用卡支付 ¥{amount}")
        print(f"卡号: ****-****-****-{self.card_number[-4:]}")
        print(f"持卡人: {self.holder_name}")
        return True

    def get_payment_type(self):
        return "信用卡"

# 支付宝支付策略
class AlipayPayment(PaymentStrategy):
    """支付宝支付策略"""
    def __init__(self, account):
        self.account = account

    def pay(self, amount):
        print(f"使用支付宝支付 ¥{amount}")
        print(f"账户: {self.account}")
        return True

    def get_payment_type(self):
        return "支付宝"

# 微信支付策略
class WechatPayment(PaymentStrategy):
    """微信支付策略"""
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def pay(self, amount):
        print(f"使用微信支付 ¥{amount}")
        print(f"手机号: {self.phone_number}")
        return True

    def get_payment_type(self):
        return "微信支付"

# 银行转账策略
class BankTransferPayment(PaymentStrategy):
    """银行转账策略"""
    def __init__(self, account_number, bank_name):
        self.account_number = account_number
        self.bank_name = bank_name

    def pay(self, amount):
        print(f"使用银行转账支付 ¥{amount}")
        print(f"银行: {self.bank_name}")
        print(f"账号: ****{self.account_number[-4:]}")
        return True

    def get_payment_type(self):
        return "银行转账"

# 购物车上下文
class ShoppingCart:
    """购物车上下文"""
    def __init__(self):
        self.items = []
        self.payment_strategy = None

    def add_item(self, item, price):
        """添加商品"""
        self.items.append({"item": item, "price": price})
        print(f"添加商品: {item} - ¥{price}")

    def remove_item(self, item):
        """移除商品"""
        self.items = [i for i in self.items if i["item"] != item]
        print(f"移除商品: {item}")

    def get_total(self):
        """计算总价"""
        return sum(item["price"] for item in self.items)

    def set_payment_strategy(self, strategy: PaymentStrategy):
        """设置支付策略"""
        self.payment_strategy = strategy
        print(f"选择支付方式: {strategy.get_payment_type()}")

    def checkout(self):
        """结账"""
        if not self.payment_strategy:
            print("请选择支付方式")
            return False

        total = self.get_total()
        print(f"\n=== 结账 ===")
        print("商品清单:")
        for item in self.items:
            print(f"  {item['item']}: ¥{item['price']}")
        print(f"总计: ¥{total}")
        print()

        success = self.payment_strategy.pay(total)
        if success:
            print("支付成功！")
            self.items.clear()
        return success

# 使用示例
def demo_payment_strategy():
    """支付策略演示"""
    # 创建购物车
    cart = ShoppingCart()

    # 添加商品
    cart.add_item("笔记本电脑", 5999)
    cart.add_item("鼠标", 199)
    cart.add_item("键盘", 299)

    # 创建支付策略
    credit_card = CreditCardPayment("1234567890123456", "张三", "123")
    alipay = AlipayPayment("zhangsan@example.com")
    wechat = WechatPayment("138****8888")
    bank_transfer = BankTransferPayment("6222021234567890", "中国银行")

    # 尝试不同的支付方式
    payment_methods = [credit_card, alipay, wechat, bank_transfer]

    for i, payment in enumerate(payment_methods, 1):
        print(f"\n=== 支付方式 {i} ===")
        cart.set_payment_strategy(payment)

        if i < len(payment_methods):
            # 前几种方式只是演示，不真正结账
            print(f"总金额: ¥{cart.get_total()}")
            print(f"支付方式: {payment.get_payment_type()}")
        else:
            # 最后一种方式真正结账
            cart.checkout()
```

### 压缩策略示例
```python
import zlib
import gzip
import bz2

# 压缩策略接口
class CompressionStrategy(ABC):
    """压缩策略接口"""
    @abstractmethod
    def compress(self, data):
        pass

    @abstractmethod
    def decompress(self, compressed_data):
        pass

    @abstractmethod
    def get_name(self):
        pass

# ZIP压缩策略
class ZipCompressionStrategy(CompressionStrategy):
    """ZIP压缩策略"""
    def compress(self, data):
        return zlib.compress(data.encode('utf-8'))

    def decompress(self, compressed_data):
        return zlib.decompress(compressed_data).decode('utf-8')

    def get_name(self):
        return "ZIP压缩"

# GZIP压缩策略
class GzipCompressionStrategy(CompressionStrategy):
    """GZIP压缩策略"""
    def compress(self, data):
        return gzip.compress(data.encode('utf-8'))

    def decompress(self, compressed_data):
        return gzip.decompress(compressed_data).decode('utf-8')

    def get_name(self):
        return "GZIP压缩"

# BZ2压缩策略
class Bz2CompressionStrategy(CompressionStrategy):
    """BZ2压缩策略"""
    def compress(self, data):
        return bz2.compress(data.encode('utf-8'))

    def decompress(self, compressed_data):
        return bz2.decompress(compressed_data).decode('utf-8')

    def get_name(self):
        return "BZ2压缩"

# 文件压缩上下文
class FileCompressor:
    """文件压缩上下文"""
    def __init__(self, strategy: CompressionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: CompressionStrategy):
        """设置压缩策略"""
        self._strategy = strategy

    def compress_data(self, data):
        """压缩数据"""
        original_size = len(data.encode('utf-8'))
        compressed_data = self._strategy.compress(data)
        compressed_size = len(compressed_data)
        ratio = (1 - compressed_size / original_size) * 100

        print(f"{self._strategy.get_name()}:")
        print(f"  原始大小: {original_size} 字节")
        print(f"  压缩大小: {compressed_size} 字节")
        print(f"  压缩率: {ratio:.2f}%")

        return compressed_data

    def decompress_data(self, compressed_data):
        """解压数据"""
        return self._strategy.decompress(compressed_data)

# 使用示例
def demo_compression_strategy():
    """压缩策略演示"""
    # 测试数据
    test_data = """
    这是一个测试文件，用于演示不同的压缩策略。
    策略模式允许我们在运行时选择不同的算法。
    在这个例子中，我们可以选择不同的压缩算法来压缩数据。
    每种压缩算法都有其特点和适用场景。
    """ * 10  # 重复10次以增加数据量

    # 创建压缩策略
    strategies = [
        ZipCompressionStrategy(),
        GzipCompressionStrategy(),
        Bz2CompressionStrategy()
    ]

    compressor = FileCompressor(strategies[0])

    print("=== 压缩策略比较 ===")
    compressed_results = []

    for strategy in strategies:
        compressor.set_strategy(strategy)
        compressed_data = compressor.compress_data(test_data)
        compressed_results.append((strategy, compressed_data))
        print()

    # 验证解压
    print("=== 解压验证 ===")
    for strategy, compressed_data in compressed_results:
        compressor.set_strategy(strategy)
        decompressed_data = compressor.decompress_data(compressed_data)
        is_correct = decompressed_data == test_data
        print(f"{strategy.get_name()}: 解压{'成功' if is_correct else '失败'}")
```

## 运行示例

每个示例文件都可以独立运行：

```bash
# 基础策略模式
python "01_basic_strategy.py"

# 排序算法策略
python "02_sorting_algorithms.py"

# 支付系统策略
python "03_payment_system.py"

# 数据处理策略
python "04_data_processing.py"

# 实际项目应用
python "05_real_world_examples.py"
```

## 设计原则

### 1. 单一职责原则
- 每个策略类只负责一个特定的算法实现
- 上下文类负责策略管理和委托

### 2. 开闭原则
- 对扩展开放：可以轻松添加新的策略
- 对修改关闭：添加新策略不需要修改现有代码

### 3. 依赖倒置原则
- 上下文依赖抽象策略接口
- 具体策略实现抽象接口

## 实现技巧

### 1. 策略注册机制
```python
class StrategyRegistry:
    """策略注册表"""
    _strategies = {}

    @classmethod
    def register(cls, name: str, strategy_class):
        cls._strategies[name] = strategy_class

    @classmethod
    def get_strategy(cls, name: str):
        if name in cls._strategies:
            return cls._strategies[name]()
        raise ValueError(f"Unknown strategy: {name}")

# 使用装饰器注册策略
def register_strategy(name: str):
    def decorator(strategy_class):
        StrategyRegistry.register(name, strategy_class)
        return strategy_class
    return decorator

@register_strategy("quick_sort")
class QuickSortStrategy(SortStrategy):
    pass
```

### 2. 策略缓存
```python
class CachedStrategyContext:
    def __init__(self):
        self._strategy_cache = {}

    def get_strategy(self, strategy_type: str):
        if strategy_type not in self._strategy_cache:
            self._strategy_cache[strategy_type] = self._create_strategy(strategy_type)
        return self._strategy_cache[strategy_type]
```

## 实际应用场景

### 1. 算法库
- **排序算法**: 根据数据规模和特征选择最优排序算法
- **搜索算法**: 线性搜索、二分搜索、哈希搜索
- **压缩算法**: ZIP、GZIP、LZ4等不同压缩策略

### 2. 业务系统
- **支付系统**: 信用卡、支付宝、微信支付等多种支付方式
- **物流系统**: 不同的配送策略和路径规划算法
- **定价策略**: 会员价、促销价、批发价等定价规则

### 3. 数据处理
- **验证策略**: 邮箱验证、手机号验证、身份证验证
- **转换策略**: 数据格式转换、编码转换
- **存储策略**: 文件存储、数据库存储、云存储

## 常见问题和解决方案

### 1. 策略选择复杂性
```python
# 问题：客户端需要了解所有策略的细节
# 解决方案：使用策略选择器
class StrategySelector:
    @staticmethod
    def select_best_strategy(data_characteristics):
        if data_characteristics['size'] > 10000:
            return HighPerformanceStrategy()
        elif data_characteristics['accuracy_required']:
            return HighAccuracyStrategy()
        else:
            return BalancedStrategy()
```

### 2. 策略间数据共享
```python
# 解决方案：使用上下文对象传递共享数据
class StrategyContext:
    def __init__(self):
        self.shared_data = {}
        self.strategy = None

    def execute(self, input_data):
        return self.strategy.execute(input_data, self.shared_data)
```

### 3. 策略组合使用
```python
# 解决方案：策略组合器
class StrategyComposer:
    def __init__(self):
        self.strategies = []

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def execute(self, data):
        result = data
        for strategy in self.strategies:
            result = strategy.execute(result)
        return result
```

## 最佳实践

### 1. 策略接口设计
- 保持策略接口简单明确
- 避免在策略接口中包含过多方法
- 使用泛型和类型提示提高代码可读性

### 2. 性能优化
- 对于无状态的策略使用单例模式
- 实现策略缓存机制避免重复创建
- 考虑使用策略预加载提高响应速度

### 3. 错误处理
- 为策略执行失败提供回退机制
- 实现策略验证确保输入数据的正确性
- 记录策略执行的日志便于调试

## 与其他模式的关系

- **状态模式**: 都封装行为，但策略模式关注算法替换，状态模式关注状态转换
- **模板方法模式**: 都定义算法框架，但策略模式通过组合实现，模板方法通过继承实现
- **工厂方法模式**: 可以使用工厂模式创建策略对象
- **装饰器模式**: 都可以改变对象行为，但策略模式是替换算法，装饰器是增强功能
- **命令模式**: 都封装行为，但策略模式关注算法，命令模式关注请求

## 学习路径

1. **理解概念**: 掌握策略模式的基本概念和结构
2. **简单实现**: 从简单的算法选择开始实践
3. **复杂应用**: 学习支付系统、数据处理等复杂场景
4. **性能优化**: 掌握策略缓存、选择器等优化技巧
5. **实际项目**: 在实际项目中应用策略模式

## 总结

策略模式是一种强大的行为型设计模式，它将算法的定义、创建和使用分离，使得算法可以独立于使用它的客户端而变化。通过合理使用策略模式，可以提高代码的灵活性、可扩展性和可维护性。在实际应用中，策略模式特别适用于需要在多种算法中进行选择的场景。
