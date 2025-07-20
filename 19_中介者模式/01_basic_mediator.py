#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
中介者模式基础实现

本模块演示了中介者模式的基本概念和实现方式，包括：
1. 智能家居控制系统示例
2. 设备间的协调通信
3. 场景模式的实现
4. 中介者接口的设计

作者: Assistant
日期: 2024-01-20
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from enum import Enum


class DeviceType(Enum):
    """设备类型枚举"""
    LIGHT = "灯光"
    AIR_CONDITIONER = "空调"
    CURTAIN = "窗帘"
    MUSIC_PLAYER = "音响"
    SECURITY_SYSTEM = "安防系统"


class Mediator(ABC):
    """中介者接口"""
    
    @abstractmethod
    def notify(self, sender: 'Device', event: str, data: Any = None) -> None:
        """处理设备事件通知"""
        pass
    
    @abstractmethod
    def register_device(self, device: 'Device') -> None:
        """注册设备"""
        pass


class Device(ABC):
    """设备基类"""
    
    def __init__(self, device_id: str, device_type: DeviceType, mediator: Mediator = None):
        self.device_id = device_id
        self.device_type = device_type
        self.mediator = mediator
        self.is_on = False
        
        if mediator:
            mediator.register_device(self)
    
    def set_mediator(self, mediator: Mediator) -> None:
        """设置中介者"""
        self.mediator = mediator
        mediator.register_device(self)
    
    def notify_mediator(self, event: str, data: Any = None) -> None:
        """通知中介者"""
        if self.mediator:
            self.mediator.notify(self, event, data)
    
    @abstractmethod
    def turn_on(self) -> None:
        """开启设备"""
        pass
    
    @abstractmethod
    def turn_off(self) -> None:
        """关闭设备"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """获取设备状态"""
        pass


class SmartLight(Device):
    """智能灯光设备"""
    
    def __init__(self, device_id: str, mediator: Mediator = None):
        super().__init__(device_id, DeviceType.LIGHT, mediator)
        self.brightness = 0  # 亮度 0-100
        self.color = "白色"
    
    def turn_on(self) -> None:
        """开启灯光"""
        self.is_on = True
        self.brightness = 80
        print(f"💡 {self.device_id} 已开启，亮度: {self.brightness}%")
        self.notify_mediator("light_on", {"brightness": self.brightness})
    
    def turn_off(self) -> None:
        """关闭灯光"""
        self.is_on = False
        self.brightness = 0
        print(f"💡 {self.device_id} 已关闭")
        self.notify_mediator("light_off")
    
    def set_brightness(self, brightness: int) -> None:
        """设置亮度"""
        if 0 <= brightness <= 100:
            self.brightness = brightness
            if brightness > 0:
                self.is_on = True
            print(f"💡 {self.device_id} 亮度调节至: {brightness}%")
            self.notify_mediator("brightness_changed", {"brightness": brightness})
    
    def set_color(self, color: str) -> None:
        """设置颜色"""
        self.color = color
        print(f"💡 {self.device_id} 颜色设置为: {color}")
        self.notify_mediator("color_changed", {"color": color})
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": self.device_type.value,
            "is_on": self.is_on,
            "brightness": self.brightness,
            "color": self.color
        }


class AirConditioner(Device):
    """空调设备"""
    
    def __init__(self, device_id: str, mediator: Mediator = None):
        super().__init__(device_id, DeviceType.AIR_CONDITIONER, mediator)
        self.temperature = 25  # 温度
        self.mode = "制冷"  # 制冷/制热/除湿/送风
    
    def turn_on(self) -> None:
        """开启空调"""
        self.is_on = True
        print(f"❄️ {self.device_id} 已开启，温度: {self.temperature}°C，模式: {self.mode}")
        self.notify_mediator("ac_on", {"temperature": self.temperature, "mode": self.mode})
    
    def turn_off(self) -> None:
        """关闭空调"""
        self.is_on = False
        print(f"❄️ {self.device_id} 已关闭")
        self.notify_mediator("ac_off")
    
    def set_temperature(self, temperature: int) -> None:
        """设置温度"""
        if 16 <= temperature <= 30:
            self.temperature = temperature
            print(f"❄️ {self.device_id} 温度设置为: {temperature}°C")
            self.notify_mediator("temperature_changed", {"temperature": temperature})
    
    def set_mode(self, mode: str) -> None:
        """设置模式"""
        self.mode = mode
        print(f"❄️ {self.device_id} 模式设置为: {mode}")
        self.notify_mediator("mode_changed", {"mode": mode})
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": self.device_type.value,
            "is_on": self.is_on,
            "temperature": self.temperature,
            "mode": self.mode
        }


class SmartCurtain(Device):
    """智能窗帘设备"""
    
    def __init__(self, device_id: str, mediator: Mediator = None):
        super().__init__(device_id, DeviceType.CURTAIN, mediator)
        self.position = 0  # 位置 0-100 (0=完全关闭, 100=完全打开)
    
    def turn_on(self) -> None:
        """打开窗帘"""
        self.is_on = True
        self.position = 100
        print(f"🪟 {self.device_id} 已完全打开")
        self.notify_mediator("curtain_opened", {"position": self.position})
    
    def turn_off(self) -> None:
        """关闭窗帘"""
        self.is_on = False
        self.position = 0
        print(f"🪟 {self.device_id} 已完全关闭")
        self.notify_mediator("curtain_closed", {"position": self.position})
    
    def set_position(self, position: int) -> None:
        """设置窗帘位置"""
        if 0 <= position <= 100:
            self.position = position
            self.is_on = position > 0
            print(f"🪟 {self.device_id} 位置调节至: {position}%")
            self.notify_mediator("curtain_position_changed", {"position": position})
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": self.device_type.value,
            "is_on": self.is_on,
            "position": self.position
        }


class MusicPlayer(Device):
    """音响设备"""
    
    def __init__(self, device_id: str, mediator: Mediator = None):
        super().__init__(device_id, DeviceType.MUSIC_PLAYER, mediator)
        self.volume = 50  # 音量 0-100
        self.current_song = ""
    
    def turn_on(self) -> None:
        """开启音响"""
        self.is_on = True
        self.current_song = "轻音乐播放列表"
        print(f"🎵 {self.device_id} 已开启，正在播放: {self.current_song}")
        self.notify_mediator("music_on", {"song": self.current_song, "volume": self.volume})
    
    def turn_off(self) -> None:
        """关闭音响"""
        self.is_on = False
        self.current_song = ""
        print(f"🎵 {self.device_id} 已关闭")
        self.notify_mediator("music_off")
    
    def set_volume(self, volume: int) -> None:
        """设置音量"""
        if 0 <= volume <= 100:
            self.volume = volume
            print(f"🎵 {self.device_id} 音量调节至: {volume}%")
            self.notify_mediator("volume_changed", {"volume": volume})
    
    def play_song(self, song: str) -> None:
        """播放歌曲"""
        self.current_song = song
        if not self.is_on:
            self.turn_on()
        print(f"🎵 {self.device_id} 正在播放: {song}")
        self.notify_mediator("song_changed", {"song": song})
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": self.device_type.value,
            "is_on": self.is_on,
            "volume": self.volume,
            "current_song": self.current_song
        }


class SmartHomeMediator(Mediator):
    """智能家居中介者"""
    
    def __init__(self, home_name: str):
        self.home_name = home_name
        self.devices: Dict[str, Device] = {}
        self.scenes: Dict[str, Dict[str, Any]] = {}
        self.auto_mode = True  # 自动模式
        
        # 预设场景
        self._setup_default_scenes()
    
    def _setup_default_scenes(self) -> None:
        """设置默认场景"""
        self.scenes = {
            "回家模式": {
                "description": "回家时的舒适环境",
                "actions": [
                    {"device_type": DeviceType.LIGHT, "action": "turn_on", "params": {"brightness": 70}},
                    {"device_type": DeviceType.AIR_CONDITIONER, "action": "turn_on", "params": {"temperature": 24}},
                    {"device_type": DeviceType.CURTAIN, "action": "set_position", "params": {"position": 50}},
                    {"device_type": DeviceType.MUSIC_PLAYER, "action": "turn_on", "params": {"volume": 30}}
                ]
            },
            "睡眠模式": {
                "description": "睡眠时的安静环境",
                "actions": [
                    {"device_type": DeviceType.LIGHT, "action": "set_brightness", "params": {"brightness": 10}},
                    {"device_type": DeviceType.AIR_CONDITIONER, "action": "set_temperature", "params": {"temperature": 22}},
                    {"device_type": DeviceType.CURTAIN, "action": "turn_off"},
                    {"device_type": DeviceType.MUSIC_PLAYER, "action": "turn_off"}
                ]
            },
            "离家模式": {
                "description": "离家时的节能模式",
                "actions": [
                    {"device_type": DeviceType.LIGHT, "action": "turn_off"},
                    {"device_type": DeviceType.AIR_CONDITIONER, "action": "turn_off"},
                    {"device_type": DeviceType.CURTAIN, "action": "turn_off"},
                    {"device_type": DeviceType.MUSIC_PLAYER, "action": "turn_off"}
                ]
            }
        }
    
    def register_device(self, device: Device) -> None:
        """注册设备"""
        self.devices[device.device_id] = device
        print(f"🏠 设备 {device.device_id} ({device.device_type.value}) 已注册到 {self.home_name}")
    
    def notify(self, sender: Device, event: str, data: Any = None) -> None:
        """处理设备事件通知"""
        print(f"🔔 中介者收到事件: {sender.device_id} -> {event}")
        
        if not self.auto_mode:
            return
        
        # 根据事件类型执行自动化逻辑
        if event == "light_on" and data:
            self._handle_light_on(sender, data)
        elif event == "ac_on":
            self._handle_ac_on(sender)
        elif event == "curtain_opened":
            self._handle_curtain_opened(sender)
        elif event == "music_on":
            self._handle_music_on(sender)
    
    def _handle_light_on(self, sender: Device, data: Dict[str, Any]) -> None:
        """处理灯光开启事件"""
        brightness = data.get("brightness", 0)
        if brightness > 80:
            # 亮度很高时，自动调节窗帘
            for device in self.devices.values():
                if device.device_type == DeviceType.CURTAIN and device != sender:
                    device.set_position(30)  # 适当关闭窗帘
    
    def _handle_ac_on(self, sender: Device) -> None:
        """处理空调开启事件"""
        # 空调开启时，自动关闭窗帘以提高效率
        for device in self.devices.values():
            if device.device_type == DeviceType.CURTAIN:
                if device.position > 70:
                    device.set_position(40)
    
    def _handle_curtain_opened(self, sender: Device) -> None:
        """处理窗帘打开事件"""
        # 窗帘完全打开时，自动调节灯光亮度
        for device in self.devices.values():
            if device.device_type == DeviceType.LIGHT and device.is_on:
                device.set_brightness(50)  # 降低亮度
    
    def _handle_music_on(self, sender: Device) -> None:
        """处理音响开启事件"""
        # 音响开启时，自动调节灯光为温馨模式
        for device in self.devices.values():
            if device.device_type == DeviceType.LIGHT:
                if not device.is_on:
                    device.turn_on()
                device.set_brightness(40)
                device.set_color("暖黄色")
    
    def activate_scene(self, scene_name: str) -> None:
        """激活场景"""
        if scene_name not in self.scenes:
            print(f"❌ 场景 '{scene_name}' 不存在")
            return
        
        scene = self.scenes[scene_name]
        print(f"🎬 激活场景: {scene_name} - {scene['description']}")
        
        for action in scene["actions"]:
            device_type = action["device_type"]
            action_name = action["action"]
            params = action.get("params", {})
            
            # 找到对应类型的设备并执行动作
            for device in self.devices.values():
                if device.device_type == device_type:
                    if hasattr(device, action_name):
                        method = getattr(device, action_name)
                        if params:
                            method(**params)
                        else:
                            method()
    
    def set_auto_mode(self, enabled: bool) -> None:
        """设置自动模式"""
        self.auto_mode = enabled
        status = "启用" if enabled else "禁用"
        print(f"🤖 自动模式已{status}")
    
    def get_all_device_status(self) -> List[Dict[str, Any]]:
        """获取所有设备状态"""
        return [device.get_status() for device in self.devices.values()]
    
    def get_available_scenes(self) -> List[str]:
        """获取可用场景列表"""
        return list(self.scenes.keys())


def demo_smart_home():
    """演示智能家居系统"""
    print("=" * 50)
    print("🏠 智能家居中介者演示")
    print("=" * 50)
    
    # 创建智能家居中介者
    home = SmartHomeMediator("我的智能家居")
    
    # 创建设备
    living_room_light = SmartLight("客厅主灯", home)
    bedroom_light = SmartLight("卧室台灯", home)
    main_ac = AirConditioner("客厅空调", home)
    living_room_curtain = SmartCurtain("客厅窗帘", home)
    sound_system = MusicPlayer("客厅音响", home)
    
    print(f"\n📊 可用场景: {home.get_available_scenes()}")
    
    # 演示场景模式
    print("\n🎬 场景演示:")
    home.activate_scene("回家模式")
    
    print("\n" + "-" * 30)
    print("💡 手动控制演示:")
    
    # 手动控制设备，观察自动化响应
    living_room_light.set_brightness(90)  # 高亮度，应该自动调节窗帘
    
    print("\n" + "-" * 30)
    main_ac.turn_on()  # 空调开启，应该自动调节窗帘
    
    print("\n" + "-" * 30)
    living_room_curtain.turn_on()  # 窗帘完全打开，应该自动调节灯光
    
    print("\n" + "-" * 30)
    sound_system.play_song("轻松爵士乐")  # 音响播放，应该调节灯光氛围
    
    # 切换到睡眠模式
    print("\n🌙 切换到睡眠模式:")
    home.activate_scene("睡眠模式")
    
    # 显示所有设备状态
    print("\n📊 当前设备状态:")
    for status in home.get_all_device_status():
        print(f"  {status}")


if __name__ == "__main__":
    print("🎯 中介者模式基础实现演示")
    
    demo_smart_home()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 中介者模式有效地解耦了设备间的复杂交互")
    print("=" * 50)
