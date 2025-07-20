"""
Python函数装饰器实用示例
展示常用的函数装饰器及其实际应用
"""

import time
import functools
from typing import Callable, Any

# 1. 计时装饰器
def timer(func: Callable) -> Callable:
    """计算函数执行时间的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️ {func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

# 2. 日志装饰器
def logger(func: Callable) -> Callable:
    """记录函数调用信息的装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📝 调用函数: {func.__name__}")
        print(f"📝 参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"📝 返回值: {result}")
        return result
    return wrapper

# 3. 缓存装饰器
def cache(func: Callable) -> Callable:
    """简单的缓存装饰器"""
    cache_dict = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 创建缓存键
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache_dict:
            print(f"💾 缓存命中: {func.__name__}")
            return cache_dict[key]
        
        result = func(*args, **kwargs)
        cache_dict[key] = result
        print(f"💾 缓存存储: {func.__name__}")
        return result
    
    return wrapper

# 4. 重试装饰器
def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器，支持参数配置"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        print(f"❌ 重试{max_attempts}次后仍然失败: {e}")
                        raise e
                    print(f"⚠️ 第{attempt + 1}次尝试失败: {e}, {delay}秒后重试...")
                    time.sleep(delay)
        return wrapper
    return decorator

# 5. 权限检查装饰器
def require_permission(permission: str):
    """权限检查装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 模拟权限检查
            user_permissions = ["read", "write"]  # 模拟用户权限
            
            if permission not in user_permissions:
                raise PermissionError(f"🚫 权限不足，需要 '{permission}' 权限")
            
            print(f"✅ 权限验证通过: {permission}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 使用装饰器的示例函数
@timer
@logger
def calculate_fibonacci(n: int) -> int:
    """计算斐波那契数列（递归版本）"""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

@cache
@timer
def calculate_fibonacci_cached(n: int) -> int:
    """计算斐波那契数列（带缓存）"""
    if n <= 1:
        return n
    return calculate_fibonacci_cached(n - 1) + calculate_fibonacci_cached(n - 2)

@retry(max_attempts=3, delay=0.5)
def unreliable_network_call():
    """模拟不稳定的网络请求"""
    import random
    if random.random() < 0.7:  # 70%失败率
        raise ConnectionError("网络连接失败")
    return "数据获取成功"

@require_permission("admin")
def delete_user(user_id: int):
    """删除用户（需要管理员权限）"""
    return f"用户 {user_id} 已删除"

@require_permission("read")
def view_user(user_id: int):
    """查看用户信息（需要读取权限）"""
    return f"用户 {user_id} 的信息"

def main():
    """演示各种装饰器的使用"""
    print("=== Python函数装饰器演示 ===\n")
    
    # 1. 计时和日志装饰器
    print("1. 计时和日志装饰器:")
    result = calculate_fibonacci(8)
    print(f"结果: {result}\n")
    
    # 2. 缓存装饰器
    print("2. 缓存装饰器:")
    print("第一次计算:")
    result1 = calculate_fibonacci_cached(10)
    print("第二次计算:")
    result2 = calculate_fibonacci_cached(10)
    print(f"结果: {result1}\n")
    
    # 3. 重试装饰器
    print("3. 重试装饰器:")
    try:
        result = unreliable_network_call()
        print(f"成功: {result}")
    except Exception as e:
        print(f"最终失败: {e}")
    print()
    
    # 4. 权限装饰器
    print("4. 权限装饰器:")
    try:
        # 有权限的操作
        result = view_user(123)
        print(result)
        
        # 无权限的操作
        result = delete_user(123)
        print(result)
    except PermissionError as e:
        print(e)

if __name__ == "__main__":
    main()