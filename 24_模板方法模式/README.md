# 模板方法模式 (Template Method Pattern)

模板方法模式是一种行为型设计模式，它在抽象类中定义算法的骨架，将某些步骤的具体实现延迟到子类中。这样可以让子类在不改变算法整体结构的前提下，重新定义算法中的某些特定步骤。

## 核心概念

模板方法模式的核心思想是"好莱坞原则"：不要调用我们，我们会调用你。父类控制整个算法的流程，在需要的时候调用子类的具体实现。

## 文件列表

### 01_basic_template.py
- **目的**: 模板方法模式的基础实现
- **内容**: 数据处理流程的模板方法演示
- **学习要点**: 理解模板方法的基本结构和抽象方法

### 02_data_processor.py
- **目的**: 数据处理系统的模板方法应用
- **内容**: CSV、JSON、XML等不同格式的数据处理流程
- **学习要点**: 实际业务场景中的模板方法应用

### 03_game_level.py
- **目的**: 游戏关卡系统的模板方法实现
- **内容**: 不同类型游戏关卡的统一处理流程
- **学习要点**: 钩子方法的使用和游戏开发中的应用

### 04_web_crawler.py
- **目的**: 网络爬虫系统的模板方法设计
- **内容**: 不同网站爬虫的统一处理框架
- **学习要点**: 复杂业务流程的模板方法设计

### 05_real_world_examples.py
- **目的**: 实际项目中的模板方法应用
- **内容**: 测试框架、报告生成、工作流程等实际应用
- **学习要点**: 模板方法在实际开发中的最佳实践

## 模式结构

```
抽象模板类 (AbstractTemplate)
    ├── template_method()     # 模板方法（定义算法骨架）
    ├── step1()              # 抽象方法（子类必须实现）
    ├── step2()              # 抽象方法（子类必须实现）
    ├── step3()              # 具体方法（默认实现）
    └── hook_method()        # 钩子方法（子类可选择重写）

具体实现类 (ConcreteTemplate)
    ├── step1()              # 实现抽象方法
    ├── step2()              # 实现抽象方法
    └── hook_method()        # 可选重写钩子方法
```

## 主要角色

- **抽象模板类**: 定义算法的骨架，包含模板方法、抽象方法和钩子方法
- **具体实现类**: 实现抽象方法，可选择重写钩子方法

## 模式优点

1. **代码复用**: 公共逻辑在父类中实现，避免重复代码
2. **控制反转**: 父类控制算法流程，子类只需实现具体步骤
3. **扩展性好**: 新增实现只需继承并实现抽象方法
4. **符合开闭原则**: 对扩展开放，对修改关闭

## 模式缺点

1. **类数量增加**: 每种实现都需要一个子类
2. **调试复杂**: 算法流程分散在父子类中
3. **理解成本**: 需要理解整个继承体系

## 适用场景

- **算法框架**: 定义算法的整体结构，具体步骤由子类实现
- **工作流程**: 业务流程固定，但具体操作因情况而异
- **数据处理**: 处理流程相同，但数据格式或来源不同
- **测试框架**: 测试流程固定，但测试内容和验证方式不同

## 快速开始

### 基本使用示例

```python
from abc import ABC, abstractmethod

# 抽象模板类
class DataProcessor(ABC):
    """数据处理模板类"""

    def process(self, data):
        """模板方法 - 定义数据处理的完整流程"""
        print("开始数据处理...")

        # 1. 验证数据
        if not self.validate_data(data):
            print("数据验证失败")
            return None

        # 2. 预处理数据
        processed_data = self.preprocess_data(data)

        # 3. 核心处理逻辑
        result = self.process_core(processed_data)

        # 4. 后处理（可选）
        if self.should_postprocess():
            result = self.postprocess_data(result)

        # 5. 保存结果
        self.save_result(result)

        print("数据处理完成")
        return result

    @abstractmethod
    def validate_data(self, data) -> bool:
        """验证数据 - 子类必须实现"""
        pass

    @abstractmethod
    def process_core(self, data):
        """核心处理逻辑 - 子类必须实现"""
        pass

    def preprocess_data(self, data):
        """预处理数据 - 默认实现"""
        return data

    def postprocess_data(self, data):
        """后处理数据 - 默认实现"""
        return data

    def should_postprocess(self) -> bool:
        """是否需要后处理 - 钩子方法"""
        return True

    def save_result(self, result):
        """保存结果 - 默认实现"""
        print(f"保存结果: {result}")

# 具体实现类
class NumberProcessor(DataProcessor):
    """数字处理器"""

    def validate_data(self, data) -> bool:
        return isinstance(data, (list, tuple)) and all(isinstance(x, (int, float)) for x in data)

    def process_core(self, data):
        return sum(data) / len(data)  # 计算平均值

    def should_postprocess(self) -> bool:
        return False  # 数字处理不需要后处理

# 使用示例
processor = NumberProcessor()
result = processor.process([1, 2, 3, 4, 5])
print(f"处理结果: {result}")
```

## 运行方法

```bash
# 运行基础示例
python 01_basic_template.py

# 运行数据处理示例
python 02_data_processor.py

# 运行游戏关卡示例
python 03_game_level.py

# 运行网络爬虫示例
python 04_web_crawler.py

# 运行实际应用示例
python 05_real_world_examples.py
```

## 学习建议

1. **从简单开始**: 先理解基本的模板方法结构，再学习复杂应用
2. **识别算法骨架**: 学会分析业务流程，识别固定步骤和可变步骤
3. **合理使用钩子方法**: 在需要可选功能时使用钩子方法
4. **对比其他模式**: 理解模板方法与策略模式的区别和适用场景
5. **实践应用**: 在实际项目中寻找可以应用模板方法的场景

## 实际应用场景

- **Web框架**: HTTP请求处理流程（验证→处理→响应）
- **数据处理**: ETL流程（提取→转换→加载）
- **测试框架**: 测试执行流程（准备→执行→清理→报告）
- **游戏开发**: 关卡流程、AI行为模式
- **工作流引擎**: 业务流程、审批流程
- **编译器**: 词法分析→语法分析→代码生成

## 与其他模式的关系

- **策略模式**: 模板方法用继承定义算法族，策略模式用组合
- **工厂方法**: 工厂方法是模板方法的特殊应用
- **观察者模式**: 可在模板方法的步骤中通知观察者
- **装饰器模式**: 可装饰模板方法的各个步骤

## 最佳实践

1. **保持模板方法简洁**: 避免在模板方法中包含过多逻辑
2. **明确抽象方法职责**: 每个抽象方法应该有单一、明确的职责
3. **合理使用默认实现**: 为常见操作提供默认实现
4. **文档化钩子方法**: 清楚说明钩子方法的用途和默认行为
5. **避免过深继承**: 控制继承层次，保持代码可维护性

## 注意事项

⚠️ **避免过度设计**: 不要为了使用模板方法而强行拆分简单流程
⚠️ **控制继承深度**: 避免创建过深的继承层次
⚠️ **明确方法职责**: 确保每个抽象方法有明确的单一职责
⚠️ **考虑组合替代**: 在某些情况下，组合可能比继承更灵活
```