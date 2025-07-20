"""
01_basic_state.py - 状态模式基础实现

这个示例展示了状态模式的核心概念和基本实现。
通过一个简单的开关状态机来演示状态转换的基本原理。
"""

from abc import ABC, abstractmethod
from typing import Optional


# ==================== 抽象接口 ====================

class State(ABC):
    """抽象状态接口"""
    
    @abstractmethod
    def handle(self, context: 'Context') -> None:
        """处理状态相关的行为"""
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        """获取状态名称"""
        pass


class Context(ABC):
    """抽象上下文接口"""
    
    def __init__(self, initial_state: State):
        self._state = initial_state
        print(f"🔄 初始状态: {self._state.get_state_name()}")
    
    def set_state(self, state: State) -> None:
        """设置新状态"""
        old_state = self._state.get_state_name()
        self._state = state
        new_state = self._state.get_state_name()
        print(f"🔄 状态转换: {old_state} → {new_state}")
    
    def get_current_state(self) -> State:
        """获取当前状态"""
        return self._state
    
    def request(self) -> None:
        """处理请求，委托给当前状态"""
        print(f"📝 当前状态: {self._state.get_state_name()}")
        self._state.handle(self)


# ==================== 具体实现 - 开关状态机 ====================

class SwitchContext(Context):
    """开关上下文类"""
    
    def __init__(self):
        super().__init__(OffState())
        self._power_level = 0
    
    @property
    def power_level(self) -> int:
        return self._power_level
    
    @power_level.setter
    def power_level(self, level: int) -> None:
        self._power_level = max(0, min(100, level))
        print(f"⚡ 功率设置为: {self._power_level}%")
    
    def turn_on(self) -> None:
        """开启"""
        print("🔘 执行开启操作")
        self._state.handle(self)
    
    def turn_off(self) -> None:
        """关闭"""
        print("🔘 执行关闭操作")
        self._state.handle(self)
    
    def adjust_power(self, level: int) -> None:
        """调节功率"""
        print(f"🔘 调节功率到 {level}%")
        self.power_level = level
        self._state.handle(self)


class OffState(State):
    """关闭状态"""
    
    def handle(self, context: SwitchContext) -> None:
        """处理关闭状态的行为"""
        if hasattr(context, '_last_action'):
            action = context._last_action
            if action == 'turn_on':
                print("💡 设备开启")
                context.set_state(OnState())
            elif action == 'turn_off':
                print("⚠️ 设备已经关闭")
            elif action == 'adjust_power':
                print("⚠️ 设备关闭时无法调节功率")
        else:
            # 默认行为
            print("💡 设备处于关闭状态")
    
    def get_state_name(self) -> str:
        return "关闭"


class OnState(State):
    """开启状态"""
    
    def handle(self, context: SwitchContext) -> None:
        """处理开启状态的行为"""
        if hasattr(context, '_last_action'):
            action = context._last_action
            if action == 'turn_on':
                print("⚠️ 设备已经开启")
            elif action == 'turn_off':
                print("💡 设备关闭")
                context.power_level = 0
                context.set_state(OffState())
            elif action == 'adjust_power':
                if context.power_level > 80:
                    print("🔥 功率过高，进入高功率状态")
                    context.set_state(HighPowerState())
                else:
                    print(f"⚡ 功率调节完成: {context.power_level}%")
        else:
            # 默认行为
            print(f"💡 设备开启中，当前功率: {context.power_level}%")
    
    def get_state_name(self) -> str:
        return "开启"


class HighPowerState(State):
    """高功率状态"""
    
    def handle(self, context: SwitchContext) -> None:
        """处理高功率状态的行为"""
        if hasattr(context, '_last_action'):
            action = context._last_action
            if action == 'turn_on':
                print("⚠️ 设备已经开启（高功率模式）")
            elif action == 'turn_off':
                print("💡 设备关闭")
                context.power_level = 0
                context.set_state(OffState())
            elif action == 'adjust_power':
                if context.power_level <= 80:
                    print("⚡ 功率降低，回到正常状态")
                    context.set_state(OnState())
                else:
                    print(f"🔥 高功率模式: {context.power_level}%")
        else:
            # 默认行为
            print(f"🔥 设备高功率运行: {context.power_level}%")
    
    def get_state_name(self) -> str:
        return "高功率"


# ==================== 增强版开关 - 支持更多操作 ====================

class AdvancedSwitch(Context):
    """高级开关类"""
    
    def __init__(self):
        super().__init__(StandbyState())
        self._brightness = 0
        self._last_action = None
    
    @property
    def brightness(self) -> int:
        return self._brightness
    
    @brightness.setter
    def brightness(self, value: int) -> None:
        self._brightness = max(0, min(100, value))
    
    def power_on(self) -> None:
        """开机"""
        self._last_action = 'power_on'
        self._state.handle(self)
    
    def power_off(self) -> None:
        """关机"""
        self._last_action = 'power_off'
        self._state.handle(self)
    
    def standby(self) -> None:
        """待机"""
        self._last_action = 'standby'
        self._state.handle(self)
    
    def set_brightness(self, level: int) -> None:
        """设置亮度"""
        self._last_action = 'set_brightness'
        self.brightness = level
        self._state.handle(self)


class StandbyState(State):
    """待机状态"""
    
    def handle(self, context: AdvancedSwitch) -> None:
        action = context._last_action
        if action == 'power_on':
            print("🌟 从待机状态开机")
            context.brightness = 50
            context.set_state(WorkingState())
        elif action == 'power_off':
            print("🔌 从待机状态关机")
            context.brightness = 0
            context.set_state(OffState())
        elif action == 'standby':
            print("⚠️ 已经处于待机状态")
        elif action == 'set_brightness':
            print("⚠️ 待机状态无法调节亮度")
    
    def get_state_name(self) -> str:
        return "待机"


class WorkingState(State):
    """工作状态"""
    
    def handle(self, context: AdvancedSwitch) -> None:
        action = context._last_action
        if action == 'power_on':
            print("⚠️ 设备已经开启")
        elif action == 'power_off':
            print("🔌 设备关机")
            context.brightness = 0
            context.set_state(OffState())
        elif action == 'standby':
            print("😴 进入待机状态")
            context.brightness = 10
            context.set_state(StandbyState())
        elif action == 'set_brightness':
            print(f"💡 亮度调节至: {context.brightness}%")
            if context.brightness == 0:
                print("💡 亮度为0，自动进入待机")
                context.set_state(StandbyState())
    
    def get_state_name(self) -> str:
        return "工作"


# ==================== 演示函数 ====================

def demo_basic_state():
    """基础状态模式演示"""
    print("=" * 60)
    print("🎯 状态模式基础演示 - 简单开关")
    print("=" * 60)
    
    # 创建开关
    switch = SwitchContext()
    
    # 测试状态转换
    print("\n📋 测试开关操作:")
    
    # 尝试关闭已关闭的设备
    switch._last_action = 'turn_off'
    switch.turn_off()
    
    # 开启设备
    switch._last_action = 'turn_on'
    switch.turn_on()
    
    # 调节功率
    switch._last_action = 'adjust_power'
    switch.adjust_power(50)
    
    # 调节到高功率
    switch._last_action = 'adjust_power'
    switch.adjust_power(90)
    
    # 降低功率
    switch._last_action = 'adjust_power'
    switch.adjust_power(60)
    
    # 关闭设备
    switch._last_action = 'turn_off'
    switch.turn_off()


def demo_advanced_state():
    """高级状态模式演示"""
    print("\n" + "=" * 60)
    print("🔧 高级状态模式演示 - 智能开关")
    print("=" * 60)
    
    # 创建高级开关
    switch = AdvancedSwitch()
    
    print("\n📋 测试智能开关操作:")
    
    # 从待机开机
    switch.power_on()
    
    # 调节亮度
    switch.set_brightness(80)
    
    # 进入待机
    switch.standby()
    
    # 尝试在待机时调节亮度
    switch.set_brightness(100)
    
    # 从待机开机
    switch.power_on()
    
    # 设置亮度为0（自动待机）
    switch.set_brightness(0)
    
    # 关机
    switch.power_off()


def demo_state_transitions():
    """状态转换演示"""
    print("\n" + "=" * 60)
    print("🔄 状态转换流程演示")
    print("=" * 60)
    
    switch = AdvancedSwitch()
    
    # 显示所有可能的状态转换
    transitions = [
        ("开机", lambda: switch.power_on()),
        ("调亮度70", lambda: switch.set_brightness(70)),
        ("待机", lambda: switch.standby()),
        ("开机", lambda: switch.power_on()),
        ("调亮度0", lambda: switch.set_brightness(0)),
        ("开机", lambda: switch.power_on()),
        ("关机", lambda: switch.power_off()),
    ]
    
    for i, (action, func) in enumerate(transitions, 1):
        print(f"\n{i}. 执行操作: {action}")
        func()


if __name__ == "__main__":
    # 运行基础演示
    demo_basic_state()
    
    # 运行高级演示
    demo_advanced_state()
    
    # 运行状态转换演示
    demo_state_transitions()
    
    print("\n" + "=" * 60)
    print("✅ 状态模式基础演示完成")
    print("💡 学习要点:")
    print("   - 状态模式将状态相关的行为封装在状态类中")
    print("   - 通过状态对象的切换来改变对象的行为")
    print("   - 避免了大量的条件判断语句")
    print("   - 使得状态转换逻辑更加清晰")
    print("=" * 60)
