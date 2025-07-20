"""
02_traffic_light.py - 交通信号灯状态机

这个示例展示了一个实际的状态机应用：交通信号灯系统。
演示了定时状态转换、状态持续时间管理和循环状态转换。
"""

from abc import ABC, abstractmethod
import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Callable


# ==================== 抽象接口 ====================

class TrafficLightState(ABC):
    """交通信号灯状态抽象类"""
    
    @abstractmethod
    def get_color(self) -> str:
        """获取信号灯颜色"""
        pass
    
    @abstractmethod
    def get_duration(self) -> int:
        """获取状态持续时间（秒）"""
        pass
    
    @abstractmethod
    def get_next_state(self) -> 'TrafficLightState':
        """获取下一个状态"""
        pass
    
    @abstractmethod
    def can_pass(self, vehicle_type: str = "car") -> bool:
        """判断是否可以通行"""
        pass
    
    @abstractmethod
    def get_message(self) -> str:
        """获取状态消息"""
        pass


# ==================== 具体状态类 ====================

class RedLightState(TrafficLightState):
    """红灯状态"""
    
    def get_color(self) -> str:
        return "🔴"
    
    def get_duration(self) -> int:
        return 30  # 红灯30秒
    
    def get_next_state(self) -> TrafficLightState:
        return GreenLightState()
    
    def can_pass(self, vehicle_type: str = "car") -> bool:
        # 只有紧急车辆可以通过红灯
        return vehicle_type == "emergency"
    
    def get_message(self) -> str:
        return "停止通行"


class YellowLightState(TrafficLightState):
    """黄灯状态"""
    
    def get_color(self) -> str:
        return "🟡"
    
    def get_duration(self) -> int:
        return 5  # 黄灯5秒
    
    def get_next_state(self) -> TrafficLightState:
        return RedLightState()
    
    def can_pass(self, vehicle_type: str = "car") -> bool:
        # 黄灯时谨慎通行
        return vehicle_type in ["emergency", "motorcycle"]
    
    def get_message(self) -> str:
        return "准备停车"


class GreenLightState(TrafficLightState):
    """绿灯状态"""
    
    def get_color(self) -> str:
        return "🟢"
    
    def get_duration(self) -> int:
        return 25  # 绿灯25秒
    
    def get_next_state(self) -> TrafficLightState:
        return YellowLightState()
    
    def can_pass(self, vehicle_type: str = "car") -> bool:
        # 绿灯时所有车辆都可以通行
        return True
    
    def get_message(self) -> str:
        return "可以通行"


# ==================== 交通信号灯控制器 ====================

class TrafficLight:
    """交通信号灯控制器"""
    
    def __init__(self, intersection_name: str = "十字路口"):
        self._intersection_name = intersection_name
        self._current_state = RedLightState()
        self._is_running = False
        self._timer_thread: Optional[threading.Thread] = None
        self._state_start_time = datetime.now()
        self._manual_mode = False
        self._observers: list[Callable] = []
        
        print(f"🚦 {self._intersection_name} 交通信号灯初始化")
        self._notify_observers()
    
    def add_observer(self, observer: Callable) -> None:
        """添加观察者"""
        self._observers.append(observer)
    
    def _notify_observers(self) -> None:
        """通知观察者状态变化"""
        for observer in self._observers:
            observer(self)
    
    @property
    def intersection_name(self) -> str:
        return self._intersection_name
    
    @property
    def current_color(self) -> str:
        return self._current_state.get_color()
    
    @property
    def current_message(self) -> str:
        return self._current_state.get_message()
    
    @property
    def is_running(self) -> bool:
        return self._is_running
    
    @property
    def is_manual_mode(self) -> bool:
        return self._manual_mode
    
    def get_remaining_time(self) -> int:
        """获取当前状态剩余时间"""
        if not self._is_running:
            return 0
        
        elapsed = (datetime.now() - self._state_start_time).total_seconds()
        remaining = max(0, self._current_state.get_duration() - elapsed)
        return int(remaining)
    
    def can_vehicle_pass(self, vehicle_type: str = "car") -> bool:
        """判断车辆是否可以通行"""
        return self._current_state.can_pass(vehicle_type)
    
    def start_automatic_mode(self) -> None:
        """启动自动模式"""
        if self._is_running:
            print("⚠️ 信号灯已在运行中")
            return
        
        self._is_running = True
        self._manual_mode = False
        self._state_start_time = datetime.now()
        
        print(f"🚦 {self._intersection_name} 启动自动模式")
        self._start_timer()
        self._notify_observers()
    
    def stop(self) -> None:
        """停止信号灯"""
        self._is_running = False
        if self._timer_thread and self._timer_thread.is_alive():
            self._timer_thread.join(timeout=1)
        
        print(f"🚦 {self._intersection_name} 信号灯停止")
        self._notify_observers()
    
    def switch_to_manual_mode(self) -> None:
        """切换到手动模式"""
        self._manual_mode = True
        self._is_running = False
        
        if self._timer_thread and self._timer_thread.is_alive():
            self._timer_thread.join(timeout=1)
        
        print(f"🚦 {self._intersection_name} 切换到手动模式")
        self._notify_observers()
    
    def manual_next_state(self) -> None:
        """手动切换到下一状态"""
        if not self._manual_mode:
            print("⚠️ 请先切换到手动模式")
            return
        
        self._change_state()
    
    def _start_timer(self) -> None:
        """启动定时器"""
        if self._timer_thread and self._timer_thread.is_alive():
            return
        
        self._timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self._timer_thread.start()
    
    def _timer_loop(self) -> None:
        """定时器循环"""
        while self._is_running and not self._manual_mode:
            duration = self._current_state.get_duration()
            time.sleep(duration)
            
            if self._is_running and not self._manual_mode:
                self._change_state()
    
    def _change_state(self) -> None:
        """改变状态"""
        old_state = self._current_state
        self._current_state = old_state.get_next_state()
        self._state_start_time = datetime.now()
        
        print(f"🚦 {self._intersection_name} 状态切换: "
              f"{old_state.get_color()} → {self._current_state.get_color()}")
        
        self._notify_observers()
    
    def get_status(self) -> dict:
        """获取当前状态信息"""
        return {
            'intersection': self._intersection_name,
            'color': self.current_color,
            'message': self.current_message,
            'remaining_time': self.get_remaining_time(),
            'is_running': self._is_running,
            'is_manual': self._manual_mode,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }


# ==================== 交通管理系统 ====================

class TrafficManagementSystem:
    """交通管理系统"""
    
    def __init__(self):
        self._traffic_lights: dict[str, TrafficLight] = {}
        self._vehicle_log: list[dict] = []
    
    def add_traffic_light(self, name: str, intersection: str) -> TrafficLight:
        """添加交通信号灯"""
        traffic_light = TrafficLight(intersection)
        traffic_light.add_observer(self._on_light_change)
        self._traffic_lights[name] = traffic_light
        
        print(f"📍 添加交通信号灯: {name} ({intersection})")
        return traffic_light
    
    def _on_light_change(self, traffic_light: TrafficLight) -> None:
        """信号灯状态变化回调"""
        status = traffic_light.get_status()
        print(f"📊 {status['intersection']}: {status['color']} {status['message']} "
              f"(剩余: {status['remaining_time']}秒)")
    
    def check_vehicle_passage(self, light_name: str, vehicle_type: str = "car") -> bool:
        """检查车辆是否可以通过"""
        if light_name not in self._traffic_lights:
            print(f"❌ 未找到信号灯: {light_name}")
            return False
        
        traffic_light = self._traffic_lights[light_name]
        can_pass = traffic_light.can_vehicle_pass(vehicle_type)
        
        # 记录车辆通行日志
        log_entry = {
            'timestamp': datetime.now(),
            'intersection': traffic_light.intersection_name,
            'vehicle_type': vehicle_type,
            'light_color': traffic_light.current_color,
            'can_pass': can_pass
        }
        self._vehicle_log.append(log_entry)
        
        status = "✅ 可以通行" if can_pass else "🚫 禁止通行"
        print(f"🚗 {vehicle_type} 在 {traffic_light.intersection_name}: {status}")
        
        return can_pass
    
    def get_all_status(self) -> dict:
        """获取所有信号灯状态"""
        return {name: light.get_status() 
                for name, light in self._traffic_lights.items()}
    
    def start_all_lights(self) -> None:
        """启动所有信号灯"""
        for light in self._traffic_lights.values():
            light.start_automatic_mode()
    
    def stop_all_lights(self) -> None:
        """停止所有信号灯"""
        for light in self._traffic_lights.values():
            light.stop()
    
    def get_traffic_report(self) -> dict:
        """获取交通报告"""
        total_vehicles = len(self._vehicle_log)
        passed_vehicles = sum(1 for log in self._vehicle_log if log['can_pass'])
        
        return {
            'total_vehicles': total_vehicles,
            'passed_vehicles': passed_vehicles,
            'blocked_vehicles': total_vehicles - passed_vehicles,
            'pass_rate': (passed_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0
        }


# ==================== 演示函数 ====================

def demo_single_traffic_light():
    """单个交通信号灯演示"""
    print("=" * 60)
    print("🚦 交通信号灯状态机演示")
    print("=" * 60)
    
    # 创建交通信号灯
    light = TrafficLight("主街与第一大道交叉口")
    
    # 测试手动模式
    print("\n📋 手动模式测试:")
    light.switch_to_manual_mode()
    
    # 手动切换几次状态
    for i in range(4):
        print(f"\n{i+1}. 当前状态: {light.current_color} - {light.current_message}")
        
        # 测试不同车辆通行
        vehicles = ["car", "motorcycle", "emergency"]
        for vehicle in vehicles:
            can_pass = light.can_vehicle_pass(vehicle)
            status = "✅" if can_pass else "🚫"
            print(f"   {vehicle}: {status}")
        
        if i < 3:  # 不在最后一次切换
            light.manual_next_state()
            time.sleep(1)


def demo_automatic_traffic_light():
    """自动交通信号灯演示"""
    print("\n" + "=" * 60)
    print("⏰ 自动模式演示 (10秒)")
    print("=" * 60)
    
    # 创建交通信号灯并启动自动模式
    light = TrafficLight("自动测试路口")
    
    # 添加状态监控
    def monitor_light(traffic_light):
        status = traffic_light.get_status()
        if status['is_running']:
            print(f"🚦 {status['color']} {status['message']} - 剩余 {status['remaining_time']}秒")
    
    light.add_observer(monitor_light)
    
    # 启动自动模式
    light.start_automatic_mode()
    
    # 运行10秒
    start_time = time.time()
    while time.time() - start_time < 10:
        time.sleep(1)
        # 模拟车辆通行检查
        if int(time.time() - start_time) % 3 == 0:
            light.can_vehicle_pass("car")
    
    # 停止信号灯
    light.stop()


def demo_traffic_management_system():
    """交通管理系统演示"""
    print("\n" + "=" * 60)
    print("🏙️ 交通管理系统演示")
    print("=" * 60)
    
    # 创建交通管理系统
    tms = TrafficManagementSystem()
    
    # 添加多个交通信号灯
    light1 = tms.add_traffic_light("north_south", "南北主干道")
    light2 = tms.add_traffic_light("east_west", "东西大街")
    
    # 设置为手动模式进行演示
    light1.switch_to_manual_mode()
    light2.switch_to_manual_mode()
    
    # 模拟车辆通行
    print("\n🚗 模拟车辆通行:")
    vehicles = [
        ("north_south", "car"),
        ("north_south", "emergency"),
        ("east_west", "motorcycle"),
        ("east_west", "car"),
    ]
    
    for light_name, vehicle_type in vehicles:
        tms.check_vehicle_passage(light_name, vehicle_type)
        time.sleep(0.5)
    
    # 切换信号灯状态
    print("\n🔄 切换信号灯状态:")
    light1.manual_next_state()  # 红灯 -> 绿灯
    light2.manual_next_state()  # 红灯 -> 绿灯
    
    # 再次测试车辆通行
    print("\n🚗 状态切换后的车辆通行:")
    for light_name, vehicle_type in vehicles:
        tms.check_vehicle_passage(light_name, vehicle_type)
        time.sleep(0.5)
    
    # 显示交通报告
    print("\n📊 交通报告:")
    report = tms.get_traffic_report()
    print(f"   总车辆数: {report['total_vehicles']}")
    print(f"   通行车辆: {report['passed_vehicles']}")
    print(f"   阻止车辆: {report['blocked_vehicles']}")
    print(f"   通行率: {report['pass_rate']:.1f}%")


if __name__ == "__main__":
    # 运行单个信号灯演示
    demo_single_traffic_light()
    
    # 运行自动模式演示
    demo_automatic_traffic_light()
    
    # 运行交通管理系统演示
    demo_traffic_management_system()
    
    print("\n" + "=" * 60)
    print("✅ 交通信号灯演示完成")
    print("💡 学习要点:")
    print("   - 状态机的循环转换")
    print("   - 定时状态切换的实现")
    print("   - 状态对行为的影响")
    print("   - 手动和自动模式的切换")
    print("=" * 60)
