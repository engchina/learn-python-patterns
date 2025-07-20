"""
01_basic_facade.py - 外观模式基础实现

智能家居控制系统示例
这个示例展示了如何使用外观模式来简化智能家居系统的控制。
智能家居系统包含多个独立的子系统（灯光、空调、音响、安防等），
外观模式提供了统一的控制接口，让用户可以通过简单的命令来控制整个家居环境。
"""

import time


# ==================== 子系统：灯光控制 ====================
class LightingSystem:
    """灯光控制子系统"""
    
    def __init__(self):
        self.lights = {
            "客厅": {"brightness": 0, "color": "白色", "is_on": False},
            "卧室": {"brightness": 0, "color": "白色", "is_on": False},
            "厨房": {"brightness": 0, "color": "白色", "is_on": False},
            "书房": {"brightness": 0, "color": "白色", "is_on": False}
        }
    
    def turn_on_light(self, room: str, brightness: int = 80):
        """开启指定房间的灯光"""
        if room in self.lights:
            self.lights[room]["is_on"] = True
            self.lights[room]["brightness"] = brightness
            return f"灯光系统: {room}灯光已开启，亮度{brightness}%"
        return f"灯光系统: 未找到{room}的灯光"
    
    def turn_off_light(self, room: str):
        """关闭指定房间的灯光"""
        if room in self.lights:
            self.lights[room]["is_on"] = False
            self.lights[room]["brightness"] = 0
            return f"灯光系统: {room}灯光已关闭"
        return f"灯光系统: 未找到{room}的灯光"
    
    def set_brightness(self, room: str, brightness: int):
        """设置灯光亮度"""
        if room in self.lights and self.lights[room]["is_on"]:
            self.lights[room]["brightness"] = brightness
            return f"灯光系统: {room}亮度已调节至{brightness}%"
        return f"灯光系统: {room}灯光未开启或不存在"
    
    def set_color(self, room: str, color: str):
        """设置灯光颜色"""
        if room in self.lights and self.lights[room]["is_on"]:
            self.lights[room]["color"] = color
            return f"灯光系统: {room}灯光颜色已设置为{color}"
        return f"灯光系统: {room}灯光未开启或不存在"
    
    def turn_off_all(self):
        """关闭所有灯光"""
        for room in self.lights:
            self.lights[room]["is_on"] = False
            self.lights[room]["brightness"] = 0
        return "灯光系统: 所有灯光已关闭"


# ==================== 子系统：空调控制 ====================
class AirConditioningSystem:
    """空调控制子系统"""
    
    def __init__(self):
        self.ac_units = {
            "客厅": {"temperature": 25, "mode": "关闭", "fan_speed": 1},
            "卧室": {"temperature": 25, "mode": "关闭", "fan_speed": 1},
            "书房": {"temperature": 25, "mode": "关闭", "fan_speed": 1}
        }
    
    def turn_on_ac(self, room: str, temperature: int = 24, mode: str = "制冷"):
        """开启空调"""
        if room in self.ac_units:
            self.ac_units[room]["mode"] = mode
            self.ac_units[room]["temperature"] = temperature
            return f"空调系统: {room}空调已开启，{mode}模式，温度{temperature}°C"
        return f"空调系统: 未找到{room}的空调"
    
    def turn_off_ac(self, room: str):
        """关闭空调"""
        if room in self.ac_units:
            self.ac_units[room]["mode"] = "关闭"
            return f"空调系统: {room}空调已关闭"
        return f"空调系统: 未找到{room}的空调"
    
    def set_temperature(self, room: str, temperature: int):
        """设置温度"""
        if room in self.ac_units and self.ac_units[room]["mode"] != "关闭":
            self.ac_units[room]["temperature"] = temperature
            return f"空调系统: {room}温度已设置为{temperature}°C"
        return f"空调系统: {room}空调未开启或不存在"
    
    def turn_off_all(self):
        """关闭所有空调"""
        for room in self.ac_units:
            self.ac_units[room]["mode"] = "关闭"
        return "空调系统: 所有空调已关闭"


# ==================== 子系统：音响控制 ====================
class AudioSystem:
    """音响控制子系统"""
    
    def __init__(self):
        self.is_on = False
        self.volume = 0
        self.current_source = None
        self.current_playlist = None
    
    def turn_on(self):
        """开启音响"""
        self.is_on = True
        return "音响系统: 音响已开启"
    
    def turn_off(self):
        """关闭音响"""
        self.is_on = False
        self.volume = 0
        self.current_source = None
        return "音响系统: 音响已关闭"
    
    def set_volume(self, volume: int):
        """设置音量"""
        if self.is_on:
            self.volume = max(0, min(100, volume))
            return f"音响系统: 音量已设置为{self.volume}"
        return "音响系统: 音响未开启"
    
    def play_music(self, playlist: str):
        """播放音乐"""
        if self.is_on:
            self.current_playlist = playlist
            self.current_source = "音乐"
            return f"音响系统: 正在播放播放列表 '{playlist}'"
        return "音响系统: 音响未开启"


# ==================== 子系统：安防控制 ====================
class SecuritySystem:
    """安防控制子系统"""
    
    def __init__(self):
        self.is_armed = False
        self.cameras_on = False
        self.door_locked = False
        self.alarm_on = False
    
    def arm_system(self):
        """启动安防系统"""
        self.is_armed = True
        self.cameras_on = True
        return "安防系统: 安防系统已启动，摄像头已开启"
    
    def disarm_system(self):
        """关闭安防系统"""
        self.is_armed = False
        self.alarm_on = False
        return "安防系统: 安防系统已关闭"
    
    def lock_doors(self):
        """锁门"""
        self.door_locked = True
        return "安防系统: 所有门已锁定"
    
    def unlock_doors(self):
        """开锁"""
        self.door_locked = False
        return "安防系统: 所有门已解锁"


# ==================== 外观类：智能家居控制器 ====================
class SmartHomeFacade:
    """智能家居外观类
    
    提供简化的接口来控制整个智能家居系统，
    将复杂的子系统操作封装成简单易用的场景模式。
    """
    
    def __init__(self):
        # 初始化所有子系统
        self.lighting = LightingSystem()
        self.air_conditioning = AirConditioningSystem()
        self.audio = AudioSystem()
        self.security = SecuritySystem()
    
    def arrive_home_mode(self):
        """回家模式：开启基本照明和空调，解锁门禁"""
        print("🏠 启动回家模式...")
        actions = [
            self.security.disarm_system(),
            self.security.unlock_doors(),
            self.lighting.turn_on_light("客厅", 70),
            self.lighting.turn_on_light("厨房", 60),
            self.air_conditioning.turn_on_ac("客厅", 24, "制冷"),
            self.audio.turn_on(),
            self.audio.set_volume(30),
            self.audio.play_music("轻松音乐")
        ]
        
        for action in actions:
            print(f"  ✓ {action}")
            time.sleep(0.1)  # 模拟设备响应时间
        
        print("🎉 回家模式设置完成！欢迎回家！")
    
    def leave_home_mode(self):
        """离家模式：关闭所有设备，启动安防"""
        print("🚪 启动离家模式...")
        actions = [
            self.lighting.turn_off_all(),
            self.air_conditioning.turn_off_all(),
            self.audio.turn_off(),
            self.security.lock_doors(),
            self.security.arm_system()
        ]
        
        for action in actions:
            print(f"  ✓ {action}")
            time.sleep(0.1)
        
        print("🔒 离家模式设置完成！家已安全锁定！")
    
    def sleep_mode(self):
        """睡眠模式：调暗灯光，调节空调，播放轻音乐"""
        print("🌙 启动睡眠模式...")
        actions = [
            self.lighting.turn_off_light("客厅"),
            self.lighting.turn_off_light("厨房"),
            self.lighting.turn_on_light("卧室", 20),
            self.lighting.set_color("卧室", "暖黄色"),
            self.air_conditioning.turn_on_ac("卧室", 26, "制冷"),
            self.audio.set_volume(15),
            self.audio.play_music("睡眠音乐"),
            self.security.lock_doors()
        ]
        
        for action in actions:
            print(f"  ✓ {action}")
            time.sleep(0.1)
        
        print("😴 睡眠模式设置完成！祝您好梦！")
    
    def work_mode(self):
        """工作模式：开启书房灯光和空调，播放专注音乐"""
        print("💼 启动工作模式...")
        actions = [
            self.lighting.turn_on_light("书房", 90),
            self.lighting.set_color("书房", "白色"),
            self.air_conditioning.turn_on_ac("书房", 23, "制冷"),
            self.audio.turn_on(),
            self.audio.set_volume(25),
            self.audio.play_music("专注音乐")
        ]
        
        for action in actions:
            print(f"  ✓ {action}")
            time.sleep(0.1)
        
        print("📚 工作模式设置完成！专注工作吧！")


# ==================== 使用示例 ====================
def demo_basic_facade():
    """基础外观模式演示"""
    print("=" * 60)
    print("🏠 智能家居控制系统演示 - 外观模式基础实现")
    print("=" * 60)
    
    # 创建智能家居控制器
    smart_home = SmartHomeFacade()
    
    # 演示不同的场景模式
    scenarios = [
        ("回家场景", smart_home.arrive_home_mode),
        ("工作场景", smart_home.work_mode),
        ("睡眠场景", smart_home.sleep_mode),
        ("离家场景", smart_home.leave_home_mode)
    ]
    
    for scenario_name, scenario_func in scenarios:
        print(f"\n{'='*20} {scenario_name} {'='*20}")
        scenario_func()
        print("\n" + "⏱️  等待2秒后切换到下一个场景...")
        time.sleep(2)
    
    print("\n" + "="*60)
    print("🎯 演示完成！外观模式成功简化了复杂的智能家居系统控制！")
    print("="*60)


if __name__ == "__main__":
    demo_basic_facade()
