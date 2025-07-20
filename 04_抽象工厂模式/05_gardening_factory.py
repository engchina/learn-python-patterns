"""
05_gardening_factory.py - 园艺规划抽象工厂模式

园艺主题系统示例
这个示例展示了如何使用抽象工厂模式来创建不同风格的园艺元素。
在园艺规划中，不同的园艺风格（如日式、欧式、现代）需要搭配相应的植物、工具和装饰，
抽象工厂模式可以确保同一风格的所有元素协调一致。

这是对原始 Gardening.py 的重写，保持了园艺主题但使用了更清晰的抽象工厂模式实现。
"""

from abc import ABC, abstractmethod
import random


# ==================== 抽象产品类 ====================
class Plant(ABC):
    """植物抽象基类"""
    
    def __init__(self, name: str, care_level: str):
        self.name = name
        self.care_level = care_level  # 护理难度：简单、中等、困难
        self.growth_stage = "幼苗"
        self.health = 100
    
    @abstractmethod
    def grow(self) -> str:
        """植物生长"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取植物描述"""
        pass
    
    @abstractmethod
    def get_care_instructions(self) -> str:
        """获取护理说明"""
        pass


class Tool(ABC):
    """园艺工具抽象基类"""
    
    def __init__(self, name: str, tool_type: str):
        self.name = name
        self.tool_type = tool_type  # 工具类型：浇水、修剪、挖掘
        self.durability = 100
    
    @abstractmethod
    def use(self, target: str) -> str:
        """使用工具"""
        pass
    
    @abstractmethod
    def maintain(self) -> str:
        """维护工具"""
        pass


class Decoration(ABC):
    """装饰品抽象基类"""
    
    def __init__(self, name: str, style: str):
        self.name = name
        self.style = style
        self.condition = "全新"
    
    @abstractmethod
    def place(self, location: str) -> str:
        """放置装饰品"""
        pass
    
    @abstractmethod
    def get_aesthetic_value(self) -> int:
        """获取美学价值"""
        pass


# ==================== 日式风格产品族 ====================
class JapanesePlant(Plant):
    """日式植物"""
    
    def __init__(self, name: str, care_level: str):
        super().__init__(name, care_level)
        self.zen_factor = random.randint(1, 10)  # 禅意指数
    
    def grow(self) -> str:
        """日式植物生长"""
        growth_stages = ["幼苗", "成长期", "成熟期", "开花期"]
        if self.growth_stage != "开花期":
            current_index = growth_stages.index(self.growth_stage)
            self.growth_stage = growth_stages[current_index + 1]
        
        return f"日式{self.name}静静生长，当前阶段：{self.growth_stage}，散发着宁静的禅意"
    
    def get_description(self) -> str:
        """获取日式植物描述"""
        return f"日式{self.name}：{self.care_level}护理，禅意指数{self.zen_factor}/10，体现东方美学"
    
    def get_care_instructions(self) -> str:
        """获取日式植物护理说明"""
        return f"日式{self.name}护理：需要{self.care_level}护理，保持土壤湿润，避免强光直射，定期修剪以保持形状"


class JapaneseTool(Tool):
    """日式园艺工具"""
    
    def __init__(self, name: str, tool_type: str):
        super().__init__(name, tool_type)
        self.craftsmanship = "手工制作"
    
    def use(self, target: str) -> str:
        """使用日式工具"""
        self.durability -= 5
        return f"使用精致的日式{self.name}对{target}进行{self.tool_type}，动作优雅而精准"
    
    def maintain(self) -> str:
        """维护日式工具"""
        self.durability = min(100, self.durability + 20)
        return f"用传统方法维护日式{self.name}，恢复其原有的光泽和锋利度"


class JapaneseDecoration(Decoration):
    """日式装饰品"""
    
    def __init__(self, name: str):
        super().__init__(name, "日式")
        self.harmony_level = random.randint(1, 10)
    
    def place(self, location: str) -> str:
        """放置日式装饰品"""
        return f"在{location}精心放置{self.name}，营造出宁静和谐的日式氛围"
    
    def get_aesthetic_value(self) -> int:
        """获取日式装饰品美学价值"""
        return self.harmony_level * 10


# ==================== 欧式风格产品族 ====================
class EuropeanPlant(Plant):
    """欧式植物"""
    
    def __init__(self, name: str, care_level: str):
        super().__init__(name, care_level)
        self.elegance_factor = random.randint(1, 10)  # 优雅指数
    
    def grow(self) -> str:
        """欧式植物生长"""
        growth_stages = ["幼苗", "成长期", "成熟期", "盛开期"]
        if self.growth_stage != "盛开期":
            current_index = growth_stages.index(self.growth_stage)
            self.growth_stage = growth_stages[current_index + 1]
        
        return f"欧式{self.name}优雅地生长，当前阶段：{self.growth_stage}，展现出古典的贵族气质"
    
    def get_description(self) -> str:
        """获取欧式植物描述"""
        return f"欧式{self.name}：{self.care_level}护理，优雅指数{self.elegance_factor}/10，彰显贵族风范"
    
    def get_care_instructions(self) -> str:
        """获取欧式植物护理说明"""
        return f"欧式{self.name}护理：需要{self.care_level}护理，充足阳光，定期施肥，保持良好通风"


class EuropeanTool(Tool):
    """欧式园艺工具"""
    
    def __init__(self, name: str, tool_type: str):
        super().__init__(name, tool_type)
        self.material = "优质钢材"
    
    def use(self, target: str) -> str:
        """使用欧式工具"""
        self.durability -= 3
        return f"使用精美的欧式{self.name}对{target}进行{self.tool_type}，体现出贵族般的优雅"
    
    def maintain(self) -> str:
        """维护欧式工具"""
        self.durability = min(100, self.durability + 25)
        return f"用专业方法维护欧式{self.name}，保持其贵族品质"


class EuropeanDecoration(Decoration):
    """欧式装饰品"""
    
    def __init__(self, name: str):
        super().__init__(name, "欧式")
        self.luxury_level = random.randint(1, 10)
    
    def place(self, location: str) -> str:
        """放置欧式装饰品"""
        return f"在{location}优雅地摆放{self.name}，彰显出浓郁的欧式古典风情"
    
    def get_aesthetic_value(self) -> int:
        """获取欧式装饰品美学价值"""
        return self.luxury_level * 12


# ==================== 现代风格产品族 ====================
class ModernPlant(Plant):
    """现代植物"""
    
    def __init__(self, name: str, care_level: str):
        super().__init__(name, care_level)
        self.minimalism_factor = random.randint(1, 10)  # 简约指数
    
    def grow(self) -> str:
        """现代植物生长"""
        growth_stages = ["幼苗", "成长期", "成熟期", "最佳状态"]
        if self.growth_stage != "最佳状态":
            current_index = growth_stages.index(self.growth_stage)
            self.growth_stage = growth_stages[current_index + 1]
        
        return f"现代{self.name}简洁地生长，当前阶段：{self.growth_stage}，体现出现代简约美学"
    
    def get_description(self) -> str:
        """获取现代植物描述"""
        return f"现代{self.name}：{self.care_level}护理，简约指数{self.minimalism_factor}/10，展现简约风格"
    
    def get_care_instructions(self) -> str:
        """获取现代植物护理说明"""
        return f"现代{self.name}护理：需要{self.care_level}护理，使用智能浇水系统，LED补光，自动化管理"


class ModernTool(Tool):
    """现代园艺工具"""
    
    def __init__(self, name: str, tool_type: str):
        super().__init__(name, tool_type)
        self.technology_level = random.randint(1, 5)
    
    def use(self, target: str) -> str:
        """使用现代工具"""
        self.durability -= 2
        return f"使用高科技现代{self.name}对{target}进行{self.tool_type}，效率高且精确"
    
    def maintain(self) -> str:
        """维护现代工具"""
        self.durability = min(100, self.durability + 30)
        return f"使用现代技术维护{self.name}，自动诊断并修复问题"


class ModernDecoration(Decoration):
    """现代装饰品"""
    
    def __init__(self, name: str):
        super().__init__(name, "现代")
        self.tech_integration = random.randint(1, 10)
    
    def place(self, location: str) -> str:
        """放置现代装饰品"""
        return f"在{location}简约地安装{self.name}，展现出现代科技与自然的完美融合"
    
    def get_aesthetic_value(self) -> int:
        """获取现代装饰品美学价值"""
        return self.tech_integration * 8


# ==================== 抽象工厂类 ====================
class GardenFactory(ABC):
    """园艺抽象工厂"""
    
    @abstractmethod
    def create_shade_plant(self) -> Plant:
        """创建阴生植物"""
        pass
    
    @abstractmethod
    def create_center_plant(self) -> Plant:
        """创建中心植物"""
        pass
    
    @abstractmethod
    def create_border_plant(self) -> Plant:
        """创建边缘植物"""
        pass
    
    @abstractmethod
    def create_tool(self) -> Tool:
        """创建园艺工具"""
        pass
    
    @abstractmethod
    def create_decoration(self) -> Decoration:
        """创建装饰品"""
        pass


# ==================== 具体工厂类 ====================
class JapaneseGardenFactory(GardenFactory):
    """日式园艺工厂"""
    
    def create_shade_plant(self) -> Plant:
        """创建日式阴生植物"""
        return JapanesePlant("苔藓", "简单")
    
    def create_center_plant(self) -> Plant:
        """创建日式中心植物"""
        return JapanesePlant("松树", "中等")
    
    def create_border_plant(self) -> Plant:
        """创建日式边缘植物"""
        return JapanesePlant("竹子", "简单")
    
    def create_tool(self) -> Tool:
        """创建日式园艺工具"""
        return JapaneseTool("竹制园艺刀", "修剪")
    
    def create_decoration(self) -> Decoration:
        """创建日式装饰品"""
        return JapaneseDecoration("石灯笼")


class EuropeanGardenFactory(GardenFactory):
    """欧式园艺工厂"""
    
    def create_shade_plant(self) -> Plant:
        """创建欧式阴生植物"""
        return EuropeanPlant("常春藤", "简单")
    
    def create_center_plant(self) -> Plant:
        """创建欧式中心植物"""
        return EuropeanPlant("玫瑰", "困难")
    
    def create_border_plant(self) -> Plant:
        """创建欧式边缘植物"""
        return EuropeanPlant("薰衣草", "中等")
    
    def create_tool(self) -> Tool:
        """创建欧式园艺工具"""
        return EuropeanTool("精美花剪", "修剪")
    
    def create_decoration(self) -> Decoration:
        """创建欧式装饰品"""
        return EuropeanDecoration("大理石雕像")


class ModernGardenFactory(GardenFactory):
    """现代园艺工厂"""
    
    def create_shade_plant(self) -> Plant:
        """创建现代阴生植物"""
        return ModernPlant("空气凤梨", "简单")
    
    def create_center_plant(self) -> Plant:
        """创建现代中心植物"""
        return ModernPlant("龙血树", "简单")
    
    def create_border_plant(self) -> Plant:
        """创建现代边缘植物"""
        return ModernPlant("多肉植物", "简单")
    
    def create_tool(self) -> Tool:
        """创建现代园艺工具"""
        return ModernTool("智能修剪器", "自动修剪")
    
    def create_decoration(self) -> Decoration:
        """创建现代装饰品"""
        return ModernDecoration("LED景观灯")


# ==================== 园艺规划师 ====================
class GardenPlanner:
    """园艺规划师"""
    
    def __init__(self, factory: GardenFactory):
        self.factory = factory
        self.garden_elements = {
            "plants": [],
            "tools": [],
            "decorations": []
        }
    
    def design_garden(self, garden_name: str):
        """设计花园"""
        print(f"正在设计{garden_name}...")
        print("=" * 50)
        
        # 创建植物
        shade_plant = self.factory.create_shade_plant()
        center_plant = self.factory.create_center_plant()
        border_plant = self.factory.create_border_plant()
        
        self.garden_elements["plants"] = [shade_plant, center_plant, border_plant]
        
        print("植物配置:")
        print(f"  阴生区域: {shade_plant.get_description()}")
        print(f"  中心区域: {center_plant.get_description()}")
        print(f"  边缘区域: {border_plant.get_description()}")
        
        # 创建工具
        tool = self.factory.create_tool()
        self.garden_elements["tools"] = [tool]
        print(f"\n推荐工具: {tool.name} ({tool.tool_type})")
        
        # 创建装饰品
        decoration = self.factory.create_decoration()
        self.garden_elements["decorations"] = [decoration]
        print(f"装饰元素: {decoration.name}")
        
        return {
            "shade_plant": shade_plant,
            "center_plant": center_plant,
            "border_plant": border_plant,
            "tool": tool,
            "decoration": decoration
        }
    
    def simulate_garden_maintenance(self):
        """模拟花园维护"""
        print(f"\n花园维护过程:")
        
        # 植物生长
        for plant in self.garden_elements["plants"]:
            growth_result = plant.grow()
            print(f"  {growth_result}")
        
        # 使用工具
        for tool in self.garden_elements["tools"]:
            for plant in self.garden_elements["plants"]:
                use_result = tool.use(plant.name)
                print(f"  {use_result}")
                break  # 只演示一次使用
        
        # 放置装饰品
        for decoration in self.garden_elements["decorations"]:
            place_result = decoration.place("花园中心")
            print(f"  {place_result}")
    
    def get_garden_summary(self) -> dict:
        """获取花园总结"""
        total_aesthetic_value = sum(
            decoration.get_aesthetic_value() 
            for decoration in self.garden_elements["decorations"]
        )
        
        return {
            "plants_count": len(self.garden_elements["plants"]),
            "tools_count": len(self.garden_elements["tools"]),
            "decorations_count": len(self.garden_elements["decorations"]),
            "total_aesthetic_value": total_aesthetic_value
        }


# ==================== 演示函数 ====================
def demonstrate_japanese_garden():
    """演示日式花园"""
    print("=" * 60)
    print("日式花园设计演示")
    print("=" * 60)
    
    # 创建日式工厂
    japanese_factory = JapaneseGardenFactory()
    
    # 创建规划师
    planner = GardenPlanner(japanese_factory)
    
    # 设计花园
    planner.design_garden("禅意日式花园")
    
    # 模拟维护
    planner.simulate_garden_maintenance()
    
    # 获取总结
    summary = planner.get_garden_summary()
    print(f"\n花园总结: {summary}")


def demonstrate_european_garden():
    """演示欧式花园"""
    print("\n" + "=" * 60)
    print("欧式花园设计演示")
    print("=" * 60)
    
    # 创建欧式工厂
    european_factory = EuropeanGardenFactory()
    
    # 创建规划师
    planner = GardenPlanner(european_factory)
    
    # 设计花园
    planner.design_garden("古典欧式花园")
    
    # 模拟维护
    planner.simulate_garden_maintenance()
    
    # 获取总结
    summary = planner.get_garden_summary()
    print(f"\n花园总结: {summary}")


def demonstrate_modern_garden():
    """演示现代花园"""
    print("\n" + "=" * 60)
    print("现代花园设计演示")
    print("=" * 60)
    
    # 创建现代工厂
    modern_factory = ModernGardenFactory()
    
    # 创建规划师
    planner = GardenPlanner(modern_factory)
    
    # 设计花园
    planner.design_garden("简约现代花园")
    
    # 模拟维护
    planner.simulate_garden_maintenance()
    
    # 获取总结
    summary = planner.get_garden_summary()
    print(f"\n花园总结: {summary}")


def main():
    """主函数"""
    print("抽象工厂模式演示 - 园艺规划系统")
    
    demonstrate_japanese_garden()
    demonstrate_european_garden()
    demonstrate_modern_garden()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("抽象工厂模式确保了同一风格的所有园艺元素协调一致。")
    print("=" * 60)


if __name__ == "__main__":
    main()
