"""
01_basic_strategy.py - 策略模式基础实现

这个示例展示了策略模式的核心概念和基本实现。
通过一个简单的数据处理系统来演示策略的封装和动态切换。
"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict
import random


# ==================== 抽象接口 ====================

class Strategy(ABC):
    """抽象策略接口"""
    
    @abstractmethod
    def execute(self, data: List[Any]) -> Any:
        """执行策略算法"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取策略名称"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取策略描述"""
        pass


class Context:
    """上下文类 - 策略的使用者"""
    
    def __init__(self, strategy: Strategy = None):
        self._strategy = strategy
        self._execution_history: List[Dict[str, Any]] = []
    
    def set_strategy(self, strategy: Strategy) -> None:
        """设置策略"""
        old_strategy = self._strategy.get_name() if self._strategy else "无"
        self._strategy = strategy
        print(f"🔄 策略切换: {old_strategy} → {strategy.get_name()}")
    
    def execute_strategy(self, data: List[Any]) -> Any:
        """执行当前策略"""
        if not self._strategy:
            raise ValueError("未设置策略")
        
        print(f"📊 执行策略: {self._strategy.get_name()}")
        print(f"📝 策略描述: {self._strategy.get_description()}")
        
        result = self._strategy.execute(data)
        
        # 记录执行历史
        self._execution_history.append({
            'strategy': self._strategy.get_name(),
            'data_size': len(data),
            'result': result
        })
        
        return result
    
    def get_current_strategy(self) -> Strategy:
        """获取当前策略"""
        return self._strategy
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """获取执行历史"""
        return self._execution_history.copy()


# ==================== 具体策略实现 - 数据处理 ====================

class SumStrategy(Strategy):
    """求和策略"""
    
    def execute(self, data: List[Any]) -> float:
        """计算数据总和"""
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        result = sum(numeric_data)
        print(f"📈 数据总和: {result} (处理了 {len(numeric_data)} 个数值)")
        return result
    
    def get_name(self) -> str:
        return "求和策略"
    
    def get_description(self) -> str:
        return "计算数据列表中所有数值的总和"


class AverageStrategy(Strategy):
    """平均值策略"""
    
    def execute(self, data: List[Any]) -> float:
        """计算数据平均值"""
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        if not numeric_data:
            return 0.0
        
        result = sum(numeric_data) / len(numeric_data)
        print(f"📊 数据平均值: {result:.2f} (处理了 {len(numeric_data)} 个数值)")
        return result
    
    def get_name(self) -> str:
        return "平均值策略"
    
    def get_description(self) -> str:
        return "计算数据列表中所有数值的平均值"


class MaxMinStrategy(Strategy):
    """最大最小值策略"""
    
    def execute(self, data: List[Any]) -> Dict[str, float]:
        """找出数据的最大值和最小值"""
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        if not numeric_data:
            return {'max': 0, 'min': 0}
        
        result = {
            'max': max(numeric_data),
            'min': min(numeric_data)
        }
        print(f"📏 最大值: {result['max']}, 最小值: {result['min']}")
        return result
    
    def get_name(self) -> str:
        return "最大最小值策略"
    
    def get_description(self) -> str:
        return "找出数据列表中的最大值和最小值"


class SortStrategy(Strategy):
    """排序策略"""
    
    def __init__(self, reverse: bool = False):
        self._reverse = reverse
    
    def execute(self, data: List[Any]) -> List[Any]:
        """对数据进行排序"""
        # 分离数值和非数值数据
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        other_data = [x for x in data if not isinstance(x, (int, float))]
        
        # 对数值数据排序
        sorted_numeric = sorted(numeric_data, reverse=self._reverse)
        
        # 对字符串数据排序
        string_data = [str(x) for x in other_data]
        sorted_strings = sorted(string_data, reverse=self._reverse)
        
        result = sorted_numeric + sorted_strings
        order = "降序" if self._reverse else "升序"
        print(f"🔢 数据{order}排序完成: 数值 {len(sorted_numeric)} 个, 其他 {len(sorted_strings)} 个")
        return result
    
    def get_name(self) -> str:
        order = "降序" if self._reverse else "升序"
        return f"{order}排序策略"
    
    def get_description(self) -> str:
        order = "降序" if self._reverse else "升序"
        return f"对数据列表进行{order}排序"


class FilterStrategy(Strategy):
    """过滤策略"""
    
    def __init__(self, condition: str = "positive"):
        self._condition = condition
    
    def execute(self, data: List[Any]) -> List[Any]:
        """根据条件过滤数据"""
        numeric_data = [x for x in data if isinstance(x, (int, float))]
        
        if self._condition == "positive":
            result = [x for x in numeric_data if x > 0]
            print(f"✅ 过滤正数: {len(result)} 个")
        elif self._condition == "negative":
            result = [x for x in numeric_data if x < 0]
            print(f"❌ 过滤负数: {len(result)} 个")
        elif self._condition == "even":
            result = [x for x in numeric_data if isinstance(x, int) and x % 2 == 0]
            print(f"🔢 过滤偶数: {len(result)} 个")
        elif self._condition == "odd":
            result = [x for x in numeric_data if isinstance(x, int) and x % 2 == 1]
            print(f"🔢 过滤奇数: {len(result)} 个")
        else:
            result = numeric_data
            print(f"⚠️ 未知条件，返回所有数值: {len(result)} 个")
        
        return result
    
    def get_name(self) -> str:
        condition_names = {
            "positive": "正数",
            "negative": "负数", 
            "even": "偶数",
            "odd": "奇数"
        }
        condition_name = condition_names.get(self._condition, "未知")
        return f"{condition_name}过滤策略"
    
    def get_description(self) -> str:
        condition_names = {
            "positive": "正数",
            "negative": "负数",
            "even": "偶数", 
            "odd": "奇数"
        }
        condition_name = condition_names.get(self._condition, "未知条件")
        return f"过滤出数据中的{condition_name}"


# ==================== 策略管理器 ====================

class StrategyManager:
    """策略管理器 - 管理和选择策略"""
    
    def __init__(self):
        self._strategies: Dict[str, Strategy] = {}
        self._register_default_strategies()
    
    def _register_default_strategies(self) -> None:
        """注册默认策略"""
        self.register_strategy("sum", SumStrategy())
        self.register_strategy("average", AverageStrategy())
        self.register_strategy("max_min", MaxMinStrategy())
        self.register_strategy("sort_asc", SortStrategy(reverse=False))
        self.register_strategy("sort_desc", SortStrategy(reverse=True))
        self.register_strategy("filter_positive", FilterStrategy("positive"))
        self.register_strategy("filter_negative", FilterStrategy("negative"))
        self.register_strategy("filter_even", FilterStrategy("even"))
        self.register_strategy("filter_odd", FilterStrategy("odd"))
    
    def register_strategy(self, name: str, strategy: Strategy) -> None:
        """注册策略"""
        self._strategies[name] = strategy
        print(f"📝 注册策略: {name} - {strategy.get_name()}")
    
    def get_strategy(self, name: str) -> Strategy:
        """获取策略"""
        if name not in self._strategies:
            raise ValueError(f"未找到策略: {name}")
        return self._strategies[name]
    
    def list_strategies(self) -> Dict[str, str]:
        """列出所有策略"""
        return {name: strategy.get_name() for name, strategy in self._strategies.items()}
    
    def get_strategy_info(self, name: str) -> Dict[str, str]:
        """获取策略详细信息"""
        if name not in self._strategies:
            raise ValueError(f"未找到策略: {name}")
        
        strategy = self._strategies[name]
        return {
            'name': strategy.get_name(),
            'description': strategy.get_description(),
            'key': name
        }


# ==================== 演示函数 ====================

def demo_basic_strategy():
    """基础策略模式演示"""
    print("=" * 60)
    print("🎯 策略模式基础演示 - 数据处理系统")
    print("=" * 60)
    
    # 准备测试数据
    test_data = [10, -5, 3.14, 8, -2, 15, 0, 7, -1, 12.5]
    print(f"📊 测试数据: {test_data}")
    
    # 创建上下文
    context = Context()
    
    # 创建策略管理器
    manager = StrategyManager()
    
    # 演示不同策略
    strategies_to_test = ["sum", "average", "max_min", "sort_asc", "filter_positive"]
    
    for strategy_name in strategies_to_test:
        print(f"\n" + "=" * 40)
        strategy = manager.get_strategy(strategy_name)
        context.set_strategy(strategy)
        result = context.execute_strategy(test_data)
        print(f"🎯 执行结果: {result}")
    
    # 显示执行历史
    print(f"\n" + "=" * 40)
    print("📋 执行历史:")
    history = context.get_execution_history()
    for i, record in enumerate(history, 1):
        print(f"   {i}. {record['strategy']}: 处理 {record['data_size']} 个数据")


def demo_dynamic_strategy_switching():
    """动态策略切换演示"""
    print("\n" + "=" * 60)
    print("🔄 动态策略切换演示")
    print("=" * 60)
    
    # 创建不同类型的数据
    datasets = {
        "小数据集": [1, 2, 3, 4, 5],
        "大数据集": list(range(1, 101)),
        "混合数据": [1, -2, 3.5, -4.2, 5, 0, 7, -8, 9.9],
        "随机数据": [random.randint(-50, 50) for _ in range(20)]
    }
    
    context = Context()
    manager = StrategyManager()
    
    # 根据数据特征选择不同策略
    for dataset_name, data in datasets.items():
        print(f"\n📊 处理 {dataset_name}: {len(data)} 个元素")
        print(f"   数据预览: {data[:5]}{'...' if len(data) > 5 else ''}")
        
        # 根据数据特征选择策略
        if len(data) <= 5:
            strategy_name = "sum"
        elif all(isinstance(x, int) for x in data):
            strategy_name = "filter_even"
        elif any(x < 0 for x in data if isinstance(x, (int, float))):
            strategy_name = "filter_positive"
        else:
            strategy_name = "average"
        
        strategy = manager.get_strategy(strategy_name)
        context.set_strategy(strategy)
        result = context.execute_strategy(data)
        print(f"   🎯 结果: {result}")


def demo_custom_strategy():
    """自定义策略演示"""
    print("\n" + "=" * 60)
    print("🛠️ 自定义策略演示")
    print("=" * 60)
    
    # 创建自定义策略
    class MedianStrategy(Strategy):
        """中位数策略"""
        
        def execute(self, data: List[Any]) -> float:
            numeric_data = [x for x in data if isinstance(x, (int, float))]
            if not numeric_data:
                return 0.0
            
            sorted_data = sorted(numeric_data)
            n = len(sorted_data)
            
            if n % 2 == 0:
                result = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
            else:
                result = sorted_data[n//2]
            
            print(f"📊 数据中位数: {result}")
            return result
        
        def get_name(self) -> str:
            return "中位数策略"
        
        def get_description(self) -> str:
            return "计算数据列表的中位数"
    
    # 注册自定义策略
    manager = StrategyManager()
    manager.register_strategy("median", MedianStrategy())
    
    # 使用自定义策略
    context = Context()
    test_data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
    
    strategy = manager.get_strategy("median")
    context.set_strategy(strategy)
    result = context.execute_strategy(test_data)
    
    print(f"📊 测试数据: {test_data}")
    print(f"🎯 中位数结果: {result}")


if __name__ == "__main__":
    # 运行基础演示
    demo_basic_strategy()
    
    # 运行动态切换演示
    demo_dynamic_strategy_switching()
    
    # 运行自定义策略演示
    demo_custom_strategy()
    
    print("\n" + "=" * 60)
    print("✅ 策略模式基础演示完成")
    print("💡 学习要点:")
    print("   - 策略模式将算法封装在独立的策略类中")
    print("   - 可以在运行时动态切换不同的算法")
    print("   - 避免了大量的条件判断语句")
    print("   - 使得算法的扩展和维护更加容易")
    print("=" * 60)
