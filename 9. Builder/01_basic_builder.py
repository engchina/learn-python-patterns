"""
01_basic_builder.py - 建造者模式基础实现

计算机配置系统示例
这个示例展示了如何使用建造者模式来构建复杂的计算机配置。
在计算机装配中，需要按照特定的步骤来组装不同的组件，
建造者模式可以将复杂的构建过程分解为简单的步骤。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


# ==================== 产品类 ====================
class Computer:
    """计算机产品类"""
    
    def __init__(self):
        self.cpu = None
        self.motherboard = None
        self.memory = None
        self.storage = None
        self.graphics_card = None
        self.power_supply = None
        self.case = None
        self.cooling_system = None
        self.network_card = None
        self.sound_card = None
        self.peripherals = []
        self.total_price = 0.0
        self.build_notes = []
    
    def add_peripheral(self, peripheral: str):
        """添加外设"""
        self.peripherals.append(peripheral)
    
    def add_build_note(self, note: str):
        """添加装机备注"""
        self.build_notes.append(note)
    
    def calculate_total_price(self):
        """计算总价格（简化实现）"""
        # 这里可以根据各组件的价格计算总价
        # 简化实现，使用固定价格
        component_prices = {
            "cpu": 2000,
            "motherboard": 800,
            "memory": 600,
            "storage": 500,
            "graphics_card": 3000,
            "power_supply": 400,
            "case": 300,
            "cooling_system": 200
        }
        
        total = 0
        for component, price in component_prices.items():
            if getattr(self, component):
                total += price
        
        self.total_price = total
        return total
    
    def get_specification(self) -> str:
        """获取完整配置信息"""
        spec = "计算机配置清单:\n"
        spec += "=" * 40 + "\n"
        spec += f"处理器: {self.cpu or '未配置'}\n"
        spec += f"主板: {self.motherboard or '未配置'}\n"
        spec += f"内存: {self.memory or '未配置'}\n"
        spec += f"存储: {self.storage or '未配置'}\n"
        spec += f"显卡: {self.graphics_card or '未配置'}\n"
        spec += f"电源: {self.power_supply or '未配置'}\n"
        spec += f"机箱: {self.case or '未配置'}\n"
        spec += f"散热: {self.cooling_system or '未配置'}\n"
        
        if self.network_card:
            spec += f"网卡: {self.network_card}\n"
        if self.sound_card:
            spec += f"声卡: {self.sound_card}\n"
        
        if self.peripherals:
            spec += f"外设: {', '.join(self.peripherals)}\n"
        
        spec += f"总价: ¥{self.calculate_total_price():,.2f}\n"
        
        if self.build_notes:
            spec += "\n装机备注:\n"
            for note in self.build_notes:
                spec += f"- {note}\n"
        
        return spec


# ==================== 抽象建造者 ====================
class ComputerBuilder(ABC):
    """计算机建造者抽象基类"""
    
    def __init__(self):
        self.computer = Computer()
    
    @abstractmethod
    def build_cpu(self):
        """构建处理器"""
        pass
    
    @abstractmethod
    def build_motherboard(self):
        """构建主板"""
        pass
    
    @abstractmethod
    def build_memory(self):
        """构建内存"""
        pass
    
    @abstractmethod
    def build_storage(self):
        """构建存储"""
        pass
    
    @abstractmethod
    def build_graphics_card(self):
        """构建显卡"""
        pass
    
    @abstractmethod
    def build_power_supply(self):
        """构建电源"""
        pass
    
    @abstractmethod
    def build_case(self):
        """构建机箱"""
        pass
    
    @abstractmethod
    def build_cooling_system(self):
        """构建散热系统"""
        pass
    
    def build_network_card(self):
        """构建网卡（可选）"""
        pass
    
    def build_sound_card(self):
        """构建声卡（可选）"""
        pass
    
    def add_peripherals(self):
        """添加外设（可选）"""
        pass
    
    def get_computer(self) -> Computer:
        """获取构建的计算机"""
        return self.computer


# ==================== 具体建造者类 ====================
class GamingComputerBuilder(ComputerBuilder):
    """游戏电脑建造者"""
    
    def build_cpu(self):
        """构建高性能处理器"""
        self.computer.cpu = "Intel Core i9-13900K (24核32线程, 3.0-5.8GHz)"
        self.computer.add_build_note("选择高端处理器以确保游戏性能")
    
    def build_motherboard(self):
        """构建游戏主板"""
        self.computer.motherboard = "ASUS ROG STRIX Z790-E GAMING (LGA1700, DDR5)"
        self.computer.add_build_note("选择支持超频的高端主板")
    
    def build_memory(self):
        """构建大容量高频内存"""
        self.computer.memory = "G.SKILL Trident Z5 RGB 32GB (2x16GB) DDR5-6000"
        self.computer.add_build_note("大容量高频内存确保游戏流畅运行")
    
    def build_storage(self):
        """构建高速存储"""
        self.computer.storage = "Samsung 980 PRO 2TB NVMe SSD (PCIe 4.0)"
        self.computer.add_build_note("高速SSD减少游戏加载时间")
    
    def build_graphics_card(self):
        """构建顶级显卡"""
        self.computer.graphics_card = "NVIDIA GeForce RTX 4080 SUPER 16GB"
        self.computer.add_build_note("顶级显卡支持4K高画质游戏")
    
    def build_power_supply(self):
        """构建大功率电源"""
        self.computer.power_supply = "Corsair RM850x 850W 80+ Gold 全模组"
        self.computer.add_build_note("大功率电源确保系统稳定运行")
    
    def build_case(self):
        """构建游戏机箱"""
        self.computer.case = "Corsair iCUE 5000X RGB 中塔机箱"
        self.computer.add_build_note("RGB机箱提升游戏氛围")
    
    def build_cooling_system(self):
        """构建液冷散热"""
        self.computer.cooling_system = "Corsair H150i ELITE CAPELLIX 360mm 一体式水冷"
        self.computer.add_build_note("液冷散热确保高负载下的温度控制")
    
    def build_sound_card(self):
        """构建游戏声卡"""
        self.computer.sound_card = "Creative Sound Blaster AE-7 游戏声卡"
        self.computer.add_build_note("专业声卡提升游戏音效体验")
    
    def add_peripherals(self):
        """添加游戏外设"""
        self.computer.add_peripheral("机械键盘 (Cherry MX 红轴)")
        self.computer.add_peripheral("游戏鼠标 (16000 DPI)")
        self.computer.add_peripheral("27寸 4K 144Hz 游戏显示器")
        self.computer.add_peripheral("7.1声道游戏耳机")


class OfficeComputerBuilder(ComputerBuilder):
    """办公电脑建造者"""
    
    def build_cpu(self):
        """构建节能处理器"""
        self.computer.cpu = "Intel Core i5-13400 (10核16线程, 2.5-4.6GHz)"
        self.computer.add_build_note("选择性价比高的中端处理器")
    
    def build_motherboard(self):
        """构建商用主板"""
        self.computer.motherboard = "ASUS PRIME B760M-A (LGA1700, DDR4)"
        self.computer.add_build_note("稳定可靠的商用主板")
    
    def build_memory(self):
        """构建标准内存"""
        self.computer.memory = "Kingston FURY Beast 16GB (2x8GB) DDR4-3200"
        self.computer.add_build_note("16GB内存满足日常办公需求")
    
    def build_storage(self):
        """构建办公存储"""
        self.computer.storage = "Kingston NV2 500GB NVMe SSD + 1TB HDD"
        self.computer.add_build_note("SSD+HDD组合兼顾速度和容量")
    
    def build_graphics_card(self):
        """使用集成显卡"""
        self.computer.graphics_card = "Intel UHD Graphics 730 (集成显卡)"
        self.computer.add_build_note("集成显卡满足办公显示需求")
    
    def build_power_supply(self):
        """构建节能电源"""
        self.computer.power_supply = "Seasonic Focus GX-550 550W 80+ Gold"
        self.computer.add_build_note("节能电源降低运行成本")
    
    def build_case(self):
        """构建简约机箱"""
        self.computer.case = "Fractal Design Core 1000 小机箱"
        self.computer.add_build_note("小巧机箱节省办公空间")
    
    def build_cooling_system(self):
        """构建标准散热"""
        self.computer.cooling_system = "Intel 原装散热器"
        self.computer.add_build_note("原装散热器满足办公需求")
    
    def add_peripherals(self):
        """添加办公外设"""
        self.computer.add_peripheral("无线键鼠套装")
        self.computer.add_peripheral("24寸 1080P IPS 显示器")
        self.computer.add_peripheral("网络摄像头")
        self.computer.add_peripheral("激光打印机")


# ==================== 指挥者类 ====================
class ComputerDirector:
    """计算机装配指挥者"""
    
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder
    
    def build_basic_computer(self) -> Computer:
        """构建基础配置电脑"""
        print("开始构建基础配置电脑...")
        self.builder.build_cpu()
        self.builder.build_motherboard()
        self.builder.build_memory()
        self.builder.build_storage()
        self.builder.build_graphics_card()
        self.builder.build_power_supply()
        self.builder.build_case()
        self.builder.build_cooling_system()
        print("基础配置构建完成！")
        return self.builder.get_computer()
    
    def build_full_computer(self) -> Computer:
        """构建完整配置电脑"""
        print("开始构建完整配置电脑...")
        # 构建基础组件
        self.build_basic_computer()
        
        # 添加可选组件
        self.builder.build_network_card()
        self.builder.build_sound_card()
        self.builder.add_peripherals()
        
        print("完整配置构建完成！")
        return self.builder.get_computer()


# ==================== 演示函数 ====================
def demonstrate_basic_builder():
    """演示基础建造者模式"""
    print("=" * 60)
    print("基础建造者模式演示")
    print("=" * 60)
    
    # 构建游戏电脑
    print("\n构建游戏电脑:")
    gaming_builder = GamingComputerBuilder()
    director = ComputerDirector(gaming_builder)
    gaming_computer = director.build_full_computer()
    
    print("\n" + gaming_computer.get_specification())
    
    # 构建办公电脑
    print("\n" + "=" * 60)
    print("构建办公电脑:")
    office_builder = OfficeComputerBuilder()
    director = ComputerDirector(office_builder)
    office_computer = director.build_basic_computer()
    
    print("\n" + office_computer.get_specification())


def main():
    """主函数 - 演示建造者模式的各种用法"""
    print("建造者模式演示 - 计算机配置系统")
    
    # 演示基础建造者
    demonstrate_basic_builder()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
