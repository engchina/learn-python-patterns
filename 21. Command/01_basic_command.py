"""
01_basic_command.py - 命令模式基础实现

智能家居控制系统示例
这个示例展示了命令模式的基本概念和实现方式。
通过智能家居控制系统，我们可以看到如何将用户的操作请求封装成命令对象，
实现调用者与接收者的解耦，并支持撤销操作。
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# ==================== 命令接口 ====================
class Command(ABC):
    """抽象命令接口"""
    
    @abstractmethod
    def execute(self) -> str:
        """执行命令"""
        pass
    
    @abstractmethod
    def undo(self) -> str:
        """撤销命令"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取命令描述"""
        pass


# ==================== 接收者：智能设备 ====================
class Light:
    """智能灯光设备"""
    
    def __init__(self, location: str):
        self.location = location
        self.is_on = False
        self.brightness = 0
        self.color = "白色"
    
    def turn_on(self, brightness: int = 80) -> str:
        """开启灯光"""
        self.is_on = True
        self.brightness = brightness
        return f"{self.location}的灯光已开启，亮度: {brightness}%"
    
    def turn_off(self) -> str:
        """关闭灯光"""
        self.is_on = False
        self.brightness = 0
        return f"{self.location}的灯光已关闭"
    
    def set_brightness(self, brightness: int) -> str:
        """设置亮度"""
        if self.is_on:
            old_brightness = self.brightness
            self.brightness = brightness
            return f"{self.location}的灯光亮度从{old_brightness}%调节至{brightness}%"
        return f"{self.location}的灯光未开启，无法调节亮度"
    
    def get_status(self) -> str:
        """获取状态"""
        status = "开启" if self.is_on else "关闭"
        return f"{self.location}灯光状态: {status}, 亮度: {self.brightness}%"


class AirConditioner:
    """智能空调设备"""
    
    def __init__(self, location: str):
        self.location = location
        self.is_on = False
        self.temperature = 26
        self.mode = "制冷"
    
    def turn_on(self, temperature: int = 26, mode: str = "制冷") -> str:
        """开启空调"""
        self.is_on = True
        self.temperature = temperature
        self.mode = mode
        return f"{self.location}的空调已开启，温度: {temperature}°C，模式: {mode}"
    
    def turn_off(self) -> str:
        """关闭空调"""
        self.is_on = False
        return f"{self.location}的空调已关闭"
    
    def set_temperature(self, temperature: int) -> str:
        """设置温度"""
        if self.is_on:
            old_temp = self.temperature
            self.temperature = temperature
            return f"{self.location}的空调温度从{old_temp}°C调节至{temperature}°C"
        return f"{self.location}的空调未开启，无法调节温度"
    
    def get_status(self) -> str:
        """获取状态"""
        status = "开启" if self.is_on else "关闭"
        return f"{self.location}空调状态: {status}, 温度: {self.temperature}°C, 模式: {self.mode}"


# ==================== 具体命令实现 ====================
class LightOnCommand(Command):
    """开灯命令"""
    
    def __init__(self, light: Light, brightness: int = 80):
        self.light = light
        self.brightness = brightness
        self.previous_state = None
    
    def execute(self) -> str:
        # 保存之前的状态用于撤销
        self.previous_state = {
            'is_on': self.light.is_on,
            'brightness': self.light.brightness
        }
        return self.light.turn_on(self.brightness)
    
    def undo(self) -> str:
        if self.previous_state:
            if self.previous_state['is_on']:
                self.light.turn_on(self.previous_state['brightness'])
                return f"撤销操作: {self.light.location}的灯光恢复到之前状态"
            else:
                self.light.turn_off()
                return f"撤销操作: {self.light.location}的灯光已关闭"
        return "无法撤销: 没有之前的状态信息"
    
    def get_description(self) -> str:
        return f"开启{self.light.location}的灯光(亮度{self.brightness}%)"


class LightOffCommand(Command):
    """关灯命令"""
    
    def __init__(self, light: Light):
        self.light = light
        self.previous_state = None
    
    def execute(self) -> str:
        # 保存之前的状态用于撤销
        self.previous_state = {
            'is_on': self.light.is_on,
            'brightness': self.light.brightness
        }
        return self.light.turn_off()
    
    def undo(self) -> str:
        if self.previous_state and self.previous_state['is_on']:
            self.light.turn_on(self.previous_state['brightness'])
            return f"撤销操作: {self.light.location}的灯光已重新开启"
        return f"撤销操作: {self.light.location}的灯光保持关闭状态"
    
    def get_description(self) -> str:
        return f"关闭{self.light.location}的灯光"


class AirConditionerOnCommand(Command):
    """开空调命令"""
    
    def __init__(self, ac: AirConditioner, temperature: int = 26, mode: str = "制冷"):
        self.ac = ac
        self.temperature = temperature
        self.mode = mode
        self.previous_state = None
    
    def execute(self) -> str:
        # 保存之前的状态用于撤销
        self.previous_state = {
            'is_on': self.ac.is_on,
            'temperature': self.ac.temperature,
            'mode': self.ac.mode
        }
        return self.ac.turn_on(self.temperature, self.mode)
    
    def undo(self) -> str:
        if self.previous_state:
            if self.previous_state['is_on']:
                self.ac.turn_on(self.previous_state['temperature'], self.previous_state['mode'])
                return f"撤销操作: {self.ac.location}的空调恢复到之前状态"
            else:
                self.ac.turn_off()
                return f"撤销操作: {self.ac.location}的空调已关闭"
        return "无法撤销: 没有之前的状态信息"
    
    def get_description(self) -> str:
        return f"开启{self.ac.location}的空调({self.temperature}°C, {self.mode})"


class AirConditionerOffCommand(Command):
    """关空调命令"""
    
    def __init__(self, ac: AirConditioner):
        self.ac = ac
        self.previous_state = None
    
    def execute(self) -> str:
        # 保存之前的状态用于撤销
        self.previous_state = {
            'is_on': self.ac.is_on,
            'temperature': self.ac.temperature,
            'mode': self.ac.mode
        }
        return self.ac.turn_off()
    
    def undo(self) -> str:
        if self.previous_state and self.previous_state['is_on']:
            self.ac.turn_on(self.previous_state['temperature'], self.previous_state['mode'])
            return f"撤销操作: {self.ac.location}的空调已重新开启"
        return f"撤销操作: {self.ac.location}的空调保持关闭状态"
    
    def get_description(self) -> str:
        return f"关闭{self.ac.location}的空调"


# ==================== 空命令（空对象模式） ====================
class NoCommand(Command):
    """空命令 - 用于初始化或占位"""
    
    def execute(self) -> str:
        return "执行空命令 - 无操作"
    
    def undo(self) -> str:
        return "撤销空命令 - 无操作"
    
    def get_description(self) -> str:
        return "空命令"


# ==================== 调用者：智能遥控器 ====================
class SmartRemoteControl:
    """智能遥控器 - 命令调用者"""
    
    def __init__(self):
        # 初始化7个插槽，每个插槽可以设置开启和关闭命令
        self.on_commands: List[Command] = [NoCommand() for _ in range(7)]
        self.off_commands: List[Command] = [NoCommand() for _ in range(7)]
        self.last_command: Optional[Command] = None
    
    def set_command(self, slot: int, on_command: Command, off_command: Command):
        """设置指定插槽的命令"""
        if 0 <= slot < 7:
            self.on_commands[slot] = on_command
            self.off_commands[slot] = off_command
        else:
            print(f"错误: 插槽编号必须在0-6之间，当前输入: {slot}")
    
    def on_button_pressed(self, slot: int) -> str:
        """按下开启按钮"""
        if 0 <= slot < 7:
            result = self.on_commands[slot].execute()
            self.last_command = self.on_commands[slot]
            return result
        return f"错误: 插槽编号必须在0-6之间，当前输入: {slot}"
    
    def off_button_pressed(self, slot: int) -> str:
        """按下关闭按钮"""
        if 0 <= slot < 7:
            result = self.off_commands[slot].execute()
            self.last_command = self.off_commands[slot]
            return result
        return f"错误: 插槽编号必须在0-6之间，当前输入: {slot}"
    
    def undo_button_pressed(self) -> str:
        """按下撤销按钮"""
        if self.last_command:
            result = self.last_command.undo()
            return result
        return "没有可撤销的命令"
    
    def get_remote_status(self) -> str:
        """获取遥控器状态"""
        status = ["智能遥控器状态:"]
        for i in range(7):
            on_desc = self.on_commands[i].get_description()
            off_desc = self.off_commands[i].get_description()
            status.append(f"插槽{i}: 开启[{on_desc}] 关闭[{off_desc}]")
        return "\n".join(status)


# ==================== 演示函数 ====================
def demonstrate_basic_command():
    """演示基础命令模式"""
    print("=" * 60)
    print("智能家居控制系统 - 命令模式演示")
    print("=" * 60)
    
    # 创建智能设备（接收者）
    living_room_light = Light("客厅")
    bedroom_light = Light("卧室")
    living_room_ac = AirConditioner("客厅")
    
    # 创建命令对象
    living_room_light_on = LightOnCommand(living_room_light, 90)
    living_room_light_off = LightOffCommand(living_room_light)
    bedroom_light_on = LightOnCommand(bedroom_light, 60)
    bedroom_light_off = LightOffCommand(bedroom_light)
    living_room_ac_on = AirConditionerOnCommand(living_room_ac, 24, "制冷")
    living_room_ac_off = AirConditionerOffCommand(living_room_ac)
    
    # 创建遥控器（调用者）
    remote = SmartRemoteControl()
    
    # 配置遥控器
    remote.set_command(0, living_room_light_on, living_room_light_off)
    remote.set_command(1, bedroom_light_on, bedroom_light_off)
    remote.set_command(2, living_room_ac_on, living_room_ac_off)
    
    print("\n1. 遥控器初始状态:")
    print(remote.get_remote_status())
    
    print("\n2. 执行一系列命令:")
    print(f"按下插槽0开启按钮: {remote.on_button_pressed(0)}")
    print(f"按下插槽1开启按钮: {remote.on_button_pressed(1)}")
    print(f"按下插槽2开启按钮: {remote.on_button_pressed(2)}")
    
    print("\n3. 设备当前状态:")
    print(living_room_light.get_status())
    print(bedroom_light.get_status())
    print(living_room_ac.get_status())
    
    print("\n4. 执行撤销操作:")
    print(f"撤销最后一个命令: {remote.undo_button_pressed()}")
    print(f"空调状态: {living_room_ac.get_status()}")
    
    print("\n5. 关闭一些设备:")
    print(f"按下插槽0关闭按钮: {remote.off_button_pressed(0)}")
    print(f"按下插槽1关闭按钮: {remote.off_button_pressed(1)}")
    
    print("\n6. 最终设备状态:")
    print(living_room_light.get_status())
    print(bedroom_light.get_status())
    print(living_room_ac.get_status())


if __name__ == "__main__":
    demonstrate_basic_command()
