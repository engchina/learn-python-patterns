"""
02_sorting_algorithms.py - 排序算法策略实现

这个示例展示了策略模式在排序算法中的应用。
演示了不同排序算法的性能特点和适用场景。
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
import time
import random
import copy


# ==================== 抽象策略接口 ====================

class SortStrategy(ABC):
    """排序策略抽象类"""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """排序方法"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取算法名称"""
        pass
    
    @abstractmethod
    def get_time_complexity(self) -> str:
        """获取时间复杂度"""
        pass
    
    @abstractmethod
    def get_space_complexity(self) -> str:
        """获取空间复杂度"""
        pass
    
    @abstractmethod
    def is_stable(self) -> bool:
        """是否为稳定排序"""
        pass
    
    def get_best_case_size(self) -> int:
        """获取最佳使用场景的数据规模"""
        return 1000  # 默认值


# ==================== 具体排序策略 ====================

class BubbleSortStrategy(SortStrategy):
    """冒泡排序策略"""
    
    def sort(self, data: List[int]) -> List[int]:
        """冒泡排序实现"""
        arr = data.copy()
        n = len(arr)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            
            # 如果没有交换，说明已经有序
            if not swapped:
                break
        
        return arr
    
    def get_name(self) -> str:
        return "冒泡排序"
    
    def get_time_complexity(self) -> str:
        return "O(n²) 平均和最坏, O(n) 最好"
    
    def get_space_complexity(self) -> str:
        return "O(1)"
    
    def is_stable(self) -> bool:
        return True
    
    def get_best_case_size(self) -> int:
        return 50  # 适合小数据集


class QuickSortStrategy(SortStrategy):
    """快速排序策略"""
    
    def sort(self, data: List[int]) -> List[int]:
        """快速排序实现"""
        arr = data.copy()
        self._quick_sort(arr, 0, len(arr) - 1)
        return arr
    
    def _quick_sort(self, arr: List[int], low: int, high: int) -> None:
        """快速排序递归实现"""
        if low < high:
            # 分区操作
            pi = self._partition(arr, low, high)
            
            # 递归排序分区
            self._quick_sort(arr, low, pi - 1)
            self._quick_sort(arr, pi + 1, high)
    
    def _partition(self, arr: List[int], low: int, high: int) -> int:
        """分区操作"""
        # 选择最后一个元素作为基准
        pivot = arr[high]
        i = low - 1  # 较小元素的索引
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def get_name(self) -> str:
        return "快速排序"
    
    def get_time_complexity(self) -> str:
        return "O(n log n) 平均, O(n²) 最坏"
    
    def get_space_complexity(self) -> str:
        return "O(log n)"
    
    def is_stable(self) -> bool:
        return False
    
    def get_best_case_size(self) -> int:
        return 10000  # 适合大数据集


class MergeSortStrategy(SortStrategy):
    """归并排序策略"""
    
    def sort(self, data: List[int]) -> List[int]:
        """归并排序实现"""
        arr = data.copy()
        self._merge_sort(arr, 0, len(arr) - 1)
        return arr
    
    def _merge_sort(self, arr: List[int], left: int, right: int) -> None:
        """归并排序递归实现"""
        if left < right:
            mid = (left + right) // 2
            
            # 递归排序左右两半
            self._merge_sort(arr, left, mid)
            self._merge_sort(arr, mid + 1, right)
            
            # 合并已排序的两半
            self._merge(arr, left, mid, right)
    
    def _merge(self, arr: List[int], left: int, mid: int, right: int) -> None:
        """合并操作"""
        # 创建临时数组
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        # 合并两个数组
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
        
        # 复制剩余元素
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
        
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
    
    def get_name(self) -> str:
        return "归并排序"
    
    def get_time_complexity(self) -> str:
        return "O(n log n) 所有情况"
    
    def get_space_complexity(self) -> str:
        return "O(n)"
    
    def is_stable(self) -> bool:
        return True
    
    def get_best_case_size(self) -> int:
        return 5000  # 适合中大型数据集


class HeapSortStrategy(SortStrategy):
    """堆排序策略"""
    
    def sort(self, data: List[int]) -> List[int]:
        """堆排序实现"""
        arr = data.copy()
        n = len(arr)
        
        # 构建最大堆
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        
        # 逐个提取元素
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]  # 移动当前根到末尾
            self._heapify(arr, i, 0)  # 调用heapify
        
        return arr
    
    def _heapify(self, arr: List[int], n: int, i: int) -> None:
        """堆化操作"""
        largest = i  # 初始化最大值为根
        left = 2 * i + 1
        right = 2 * i + 2
        
        # 如果左子节点存在且大于根
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        # 如果右子节点存在且大于当前最大值
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        # 如果最大值不是根
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest)
    
    def get_name(self) -> str:
        return "堆排序"
    
    def get_time_complexity(self) -> str:
        return "O(n log n) 所有情况"
    
    def get_space_complexity(self) -> str:
        return "O(1)"
    
    def is_stable(self) -> bool:
        return False
    
    def get_best_case_size(self) -> int:
        return 3000  # 适合中型数据集


class InsertionSortStrategy(SortStrategy):
    """插入排序策略"""
    
    def sort(self, data: List[int]) -> List[int]:
        """插入排序实现"""
        arr = data.copy()
        
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            
            # 移动大于key的元素
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            
            arr[j + 1] = key
        
        return arr
    
    def get_name(self) -> str:
        return "插入排序"
    
    def get_time_complexity(self) -> str:
        return "O(n²) 平均和最坏, O(n) 最好"
    
    def get_space_complexity(self) -> str:
        return "O(1)"
    
    def is_stable(self) -> bool:
        return True
    
    def get_best_case_size(self) -> int:
        return 100  # 适合小数据集


class PythonSortStrategy(SortStrategy):
    """Python内置排序策略 (Timsort)"""
    
    def sort(self, data: List[int]) -> List[int]:
        """使用Python内置排序"""
        return sorted(data)
    
    def get_name(self) -> str:
        return "Python内置排序 (Timsort)"
    
    def get_time_complexity(self) -> str:
        return "O(n log n) 平均, O(n) 最好"
    
    def get_space_complexity(self) -> str:
        return "O(n)"
    
    def is_stable(self) -> bool:
        return True
    
    def get_best_case_size(self) -> int:
        return 100000  # 适合所有规模


# ==================== 排序上下文 ====================

class SortingContext:
    """排序上下文类"""
    
    def __init__(self, strategy: SortStrategy = None):
        self._strategy = strategy
        self._performance_history: List[Dict[str, Any]] = []
    
    def set_strategy(self, strategy: SortStrategy) -> None:
        """设置排序策略"""
        self._strategy = strategy
        print(f"🔄 切换排序策略: {strategy.get_name()}")
    
    def sort_with_timing(self, data: List[int]) -> Tuple[List[int], float]:
        """执行排序并计时"""
        if not self._strategy:
            raise ValueError("未设置排序策略")
        
        start_time = time.time()
        result = self._strategy.sort(data)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 记录性能数据
        self._performance_history.append({
            'strategy': self._strategy.get_name(),
            'data_size': len(data),
            'execution_time': execution_time,
            'time_complexity': self._strategy.get_time_complexity(),
            'space_complexity': self._strategy.get_space_complexity(),
            'is_stable': self._strategy.is_stable()
        })
        
        return result, execution_time
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """获取当前策略信息"""
        if not self._strategy:
            return {}
        
        return {
            'name': self._strategy.get_name(),
            'time_complexity': self._strategy.get_time_complexity(),
            'space_complexity': self._strategy.get_space_complexity(),
            'is_stable': self._strategy.is_stable(),
            'best_case_size': self._strategy.get_best_case_size()
        }
    
    def get_performance_history(self) -> List[Dict[str, Any]]:
        """获取性能历史"""
        return self._performance_history.copy()


# ==================== 智能策略选择器 ====================

class SmartSortSelector:
    """智能排序策略选择器"""
    
    def __init__(self):
        self._strategies = {
            'bubble': BubbleSortStrategy(),
            'insertion': InsertionSortStrategy(),
            'quick': QuickSortStrategy(),
            'merge': MergeSortStrategy(),
            'heap': HeapSortStrategy(),
            'python': PythonSortStrategy()
        }
    
    def select_best_strategy(self, data_size: int, data_characteristics: Dict[str, bool] = None) -> SortStrategy:
        """根据数据特征选择最佳策略"""
        if data_characteristics is None:
            data_characteristics = {}
        
        # 根据数据规模选择
        if data_size <= 50:
            if data_characteristics.get('nearly_sorted', False):
                return self._strategies['insertion']
            else:
                return self._strategies['bubble']
        elif data_size <= 1000:
            return self._strategies['insertion']
        elif data_size <= 10000:
            if data_characteristics.get('need_stable', False):
                return self._strategies['merge']
            else:
                return self._strategies['quick']
        else:
            return self._strategies['python']  # 大数据集使用优化的内置排序
    
    def get_all_strategies(self) -> Dict[str, SortStrategy]:
        """获取所有策略"""
        return self._strategies.copy()
    
    def compare_strategies(self, data: List[int], strategies: List[str] = None) -> Dict[str, Dict[str, Any]]:
        """比较多种策略的性能"""
        if strategies is None:
            strategies = list(self._strategies.keys())
        
        results = {}
        context = SortingContext()
        
        for strategy_name in strategies:
            if strategy_name not in self._strategies:
                continue
            
            strategy = self._strategies[strategy_name]
            context.set_strategy(strategy)
            
            try:
                sorted_data, execution_time = context.sort_with_timing(data)
                results[strategy_name] = {
                    'execution_time': execution_time,
                    'strategy_info': context.get_strategy_info(),
                    'success': True
                }
            except Exception as e:
                results[strategy_name] = {
                    'error': str(e),
                    'success': False
                }
        
        return results


# ==================== 演示函数 ====================

def demo_sorting_strategies():
    """排序策略演示"""
    print("=" * 60)
    print("🔢 排序算法策略模式演示")
    print("=" * 60)
    
    # 创建测试数据
    small_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"📊 小数据集: {small_data}")
    
    # 创建排序上下文
    context = SortingContext()
    
    # 测试不同排序策略
    strategies = [
        BubbleSortStrategy(),
        InsertionSortStrategy(),
        QuickSortStrategy(),
        MergeSortStrategy(),
        PythonSortStrategy()
    ]
    
    for strategy in strategies:
        print(f"\n" + "=" * 40)
        context.set_strategy(strategy)
        
        # 显示策略信息
        info = context.get_strategy_info()
        print(f"📝 算法: {info['name']}")
        print(f"⏱️ 时间复杂度: {info['time_complexity']}")
        print(f"💾 空间复杂度: {info['space_complexity']}")
        print(f"🔄 稳定性: {'稳定' if info['is_stable'] else '不稳定'}")
        
        # 执行排序
        sorted_data, execution_time = context.sort_with_timing(small_data)
        print(f"🎯 排序结果: {sorted_data}")
        print(f"⏰ 执行时间: {execution_time:.6f} 秒")


def demo_performance_comparison():
    """性能比较演示"""
    print("\n" + "=" * 60)
    print("⚡ 排序算法性能比较")
    print("=" * 60)
    
    # 创建不同规模的测试数据
    test_sizes = [100, 500, 1000]
    selector = SmartSortSelector()
    
    for size in test_sizes:
        print(f"\n📊 数据规模: {size} 个元素")
        
        # 生成随机数据
        test_data = [random.randint(1, 1000) for _ in range(size)]
        
        # 比较策略性能（只比较适合的策略）
        if size <= 100:
            strategies_to_test = ['bubble', 'insertion', 'quick', 'python']
        elif size <= 500:
            strategies_to_test = ['insertion', 'quick', 'merge', 'python']
        else:
            strategies_to_test = ['quick', 'merge', 'heap', 'python']
        
        results = selector.compare_strategies(test_data, strategies_to_test)
        
        # 按执行时间排序
        sorted_results = sorted(
            [(name, data) for name, data in results.items() if data['success']],
            key=lambda x: x[1]['execution_time']
        )
        
        print("🏆 性能排名:")
        for i, (strategy_name, data) in enumerate(sorted_results, 1):
            strategy_info = data['strategy_info']
            print(f"   {i}. {strategy_info['name']}: {data['execution_time']:.6f} 秒")


def demo_smart_selection():
    """智能策略选择演示"""
    print("\n" + "=" * 60)
    print("🧠 智能策略选择演示")
    print("=" * 60)
    
    selector = SmartSortSelector()
    context = SortingContext()
    
    # 不同场景的数据
    scenarios = [
        {
            'name': '小数据集',
            'data': [5, 2, 8, 1, 9, 3],
            'characteristics': {}
        },
        {
            'name': '中等数据集',
            'data': list(range(100, 0, -1)),  # 逆序数据
            'characteristics': {'need_stable': True}
        },
        {
            'name': '大数据集',
            'data': [random.randint(1, 1000) for _ in range(5000)],
            'characteristics': {}
        },
        {
            'name': '近似有序数据',
            'data': list(range(1, 51)) + [random.randint(1, 100) for _ in range(5)],
            'characteristics': {'nearly_sorted': True}
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 场景: {scenario['name']}")
        print(f"📊 数据规模: {len(scenario['data'])} 个元素")
        
        # 智能选择策略
        best_strategy = selector.select_best_strategy(
            len(scenario['data']), 
            scenario['characteristics']
        )
        
        context.set_strategy(best_strategy)
        info = context.get_strategy_info()
        
        print(f"🎯 推荐策略: {info['name']}")
        print(f"📝 选择理由: {info['time_complexity']}")
        
        # 执行排序
        sorted_data, execution_time = context.sort_with_timing(scenario['data'])
        print(f"⏰ 执行时间: {execution_time:.6f} 秒")
        print(f"✅ 排序完成: {len(sorted_data)} 个元素")


if __name__ == "__main__":
    # 运行排序策略演示
    demo_sorting_strategies()
    
    # 运行性能比较演示
    demo_performance_comparison()
    
    # 运行智能选择演示
    demo_smart_selection()
    
    print("\n" + "=" * 60)
    print("✅ 排序算法策略演示完成")
    print("💡 学习要点:")
    print("   - 不同排序算法适用于不同的数据规模和特征")
    print("   - 策略模式使算法选择更加灵活")
    print("   - 可以根据数据特征智能选择最优策略")
    print("   - 性能测试帮助验证策略选择的正确性")
    print("=" * 60)
