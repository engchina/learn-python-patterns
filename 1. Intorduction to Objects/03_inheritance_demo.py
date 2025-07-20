"""
03_inheritance_demo.py - 继承机制的深入理解

这个示例通过动物分类系统展示继承的核心概念：
- 基类和派生类的关系
- 方法重写和扩展
- super()的正确使用
- 继承层次的设计
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime


# ==================== 抽象基类 ====================
class Animal(ABC):
    """动物抽象基类 - 定义所有动物的共同特征"""
    
    def __init__(self, name: str, species: str, age: int, weight: float):
        """
        初始化动物对象
        
        参数:
            name: 动物名称
            species: 物种
            age: 年龄
            weight: 体重(kg)
        """
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.health_status = "健康"
        self.birth_date = datetime.now()
        
        print(f"🐾 {species} {name} 已加入动物园")
    
    @abstractmethod
    def make_sound(self) -> str:
        """发出声音 - 抽象方法，子类必须实现"""
        pass
    
    @abstractmethod
    def get_diet_type(self) -> str:
        """获取饮食类型 - 抽象方法"""
        pass
    
    def eat(self, food: str) -> str:
        """吃东西 - 通用方法"""
        return f"{self.name} 正在吃 {food}"
    
    def sleep(self) -> str:
        """睡觉 - 通用方法"""
        return f"{self.name} 正在睡觉 💤"
    
    def get_basic_info(self) -> str:
        """获取基本信息"""
        return (f"🐾 {self.name} ({self.species})\n"
                f"   年龄: {self.age}岁\n"
                f"   体重: {self.weight}kg\n"
                f"   健康状态: {self.health_status}\n"
                f"   饮食类型: {self.get_diet_type()}")
    
    def __str__(self) -> str:
        return f"{self.species}({self.name})"


# ==================== 哺乳动物类 ====================
class Mammal(Animal):
    """哺乳动物类 - 继承自Animal"""
    
    def __init__(self, name: str, species: str, age: int, weight: float, 
                 fur_color: str, is_warm_blooded: bool = True):
        """
        初始化哺乳动物
        
        参数:
            name: 名称
            species: 物种
            age: 年龄
            weight: 体重
            fur_color: 毛发颜色
            is_warm_blooded: 是否温血动物
        """
        # 调用父类构造方法
        super().__init__(name, species, age, weight)
        
        # 哺乳动物特有属性
        self.fur_color = fur_color
        self.is_warm_blooded = is_warm_blooded
        self.milk_production = False  # 是否产奶
    
    def nurse_young(self) -> str:
        """哺育幼崽 - 哺乳动物特有方法"""
        if self.milk_production:
            return f"{self.name} 正在哺育幼崽 🍼"
        return f"{self.name} 目前不在哺乳期"
    
    def get_diet_type(self) -> str:
        """获取饮食类型 - 提供默认实现"""
        return "杂食性"
    
    def get_basic_info(self) -> str:
        """重写基本信息方法，添加哺乳动物特有信息"""
        base_info = super().get_basic_info()
        mammal_info = (f"   毛发颜色: {self.fur_color}\n"
                      f"   温血动物: {'是' if self.is_warm_blooded else '否'}\n"
                      f"   哺乳状态: {'哺乳期' if self.milk_production else '非哺乳期'}")
        return base_info + "\n" + mammal_info


# ==================== 具体动物类 ====================
class Dog(Mammal):
    """狗类 - 继承自Mammal"""
    
    def __init__(self, name: str, age: int, weight: float, fur_color: str, breed: str):
        """
        初始化狗对象
        
        参数:
            name: 狗名
            age: 年龄
            weight: 体重
            fur_color: 毛色
            breed: 品种
        """
        super().__init__(name, "狗", age, weight, fur_color)
        self.breed = breed
        self.loyalty_level = 10  # 忠诚度(1-10)
        self.tricks_learned: List[str] = []
    
    def make_sound(self) -> str:
        """狗的叫声"""
        return f"{self.name}: 汪汪汪! 🐕"
    
    def get_diet_type(self) -> str:
        """狗的饮食类型"""
        return "肉食性"
    
    def learn_trick(self, trick: str):
        """学习技能"""
        if trick not in self.tricks_learned:
            self.tricks_learned.append(trick)
            print(f"🎾 {self.name} 学会了新技能: {trick}")
        else:
            print(f"🎾 {self.name} 已经会 {trick} 了")
    
    def perform_trick(self, trick: str) -> str:
        """表演技能"""
        if trick in self.tricks_learned:
            return f"🎪 {self.name} 正在表演: {trick}"
        return f"😅 {self.name} 还不会 {trick}"
    
    def fetch(self) -> str:
        """捡球游戏"""
        return f"🎾 {self.name} 兴奋地去捡球了!"
    
    def guard(self) -> str:
        """看门"""
        return f"🛡️  {self.name} 正在警惕地看门"


class Cat(Mammal):
    """猫类 - 继承自Mammal"""
    
    def __init__(self, name: str, age: int, weight: float, fur_color: str, 
                 is_indoor: bool = True):
        """
        初始化猫对象
        
        参数:
            name: 猫名
            age: 年龄
            weight: 体重
            fur_color: 毛色
            is_indoor: 是否室内猫
        """
        super().__init__(name, "猫", age, weight, fur_color)
        self.is_indoor = is_indoor
        self.independence_level = 8  # 独立性(1-10)
        self.favorite_spots: List[str] = ["阳台", "沙发"]
    
    def make_sound(self) -> str:
        """猫的叫声"""
        return f"{self.name}: 喵喵喵~ 🐱"
    
    def get_diet_type(self) -> str:
        """猫的饮食类型"""
        return "肉食性"
    
    def purr(self) -> str:
        """呼噜声"""
        return f"😸 {self.name} 满足地发出呼噜声"
    
    def climb(self, target: str) -> str:
        """爬高"""
        return f"🧗 {self.name} 敏捷地爬上了 {target}"
    
    def hunt(self) -> str:
        """狩猎"""
        if not self.is_indoor:
            return f"🏹 {self.name} 正在户外狩猎"
        return f"🏹 {self.name} 在家里'狩猎'玩具老鼠"
    
    def add_favorite_spot(self, spot: str):
        """添加喜欢的地点"""
        if spot not in self.favorite_spots:
            self.favorite_spots.append(spot)
            print(f"📍 {self.name} 现在喜欢在 {spot} 待着")


class Elephant(Mammal):
    """大象类 - 继承自Mammal"""
    
    def __init__(self, name: str, age: int, weight: float, trunk_length: float):
        """
        初始化大象对象
        
        参数:
            name: 大象名
            age: 年龄
            weight: 体重
            trunk_length: 象鼻长度(cm)
        """
        super().__init__(name, "大象", age, weight, "灰色")
        self.trunk_length = trunk_length
        self.memory_capacity = 10  # 记忆力(1-10)
        self.herd_members: List[str] = []
    
    def make_sound(self) -> str:
        """大象的叫声"""
        return f"{self.name}: 嗷呜呜呜! 🐘"
    
    def get_diet_type(self) -> str:
        """大象的饮食类型"""
        return "草食性"
    
    def use_trunk(self, action: str) -> str:
        """使用象鼻"""
        return f"🐘 {self.name} 用象鼻 {action}"
    
    def spray_water(self) -> str:
        """喷水"""
        return f"💦 {self.name} 用象鼻喷水洗澡"
    
    def remember_friend(self, friend_name: str):
        """记住朋友"""
        if friend_name not in self.herd_members:
            self.herd_members.append(friend_name)
            print(f"🧠 {self.name} 记住了朋友: {friend_name}")
    
    def trumpet(self) -> str:
        """发出号角声"""
        return f"📯 {self.name} 发出响亮的号角声，呼唤同伴"


# ==================== 鸟类 ====================
class Bird(Animal):
    """鸟类 - 继承自Animal"""
    
    def __init__(self, name: str, species: str, age: int, weight: float,
                 wingspan: float, can_fly: bool = True):
        """
        初始化鸟类
        
        参数:
            name: 鸟名
            species: 物种
            age: 年龄
            weight: 体重
            wingspan: 翼展(cm)
            can_fly: 是否会飞
        """
        super().__init__(name, species, age, weight)
        self.wingspan = wingspan
        self.can_fly = can_fly
        self.nest_location = "未知"
        self.migration_distance = 0  # 迁徙距离(km)
    
    def get_diet_type(self) -> str:
        """鸟类饮食类型"""
        return "杂食性"
    
    def fly(self) -> str:
        """飞行"""
        if self.can_fly:
            return f"🕊️  {self.name} 展开翅膀飞翔"
        return f"🐧 {self.name} 不会飞，但可以快速奔跑"
    
    def build_nest(self, location: str):
        """筑巢"""
        self.nest_location = location
        print(f"🏠 {self.name} 在 {location} 筑了一个巢")
    
    def get_basic_info(self) -> str:
        """重写基本信息，添加鸟类特有信息"""
        base_info = super().get_basic_info()
        bird_info = (f"   翼展: {self.wingspan}cm\n"
                    f"   飞行能力: {'会飞' if self.can_fly else '不会飞'}\n"
                    f"   巢穴位置: {self.nest_location}")
        return base_info + "\n" + bird_info


class Eagle(Bird):
    """老鹰类 - 继承自Bird"""
    
    def __init__(self, name: str, age: int, weight: float, wingspan: float):
        super().__init__(name, "老鹰", age, weight, wingspan, True)
        self.hunting_success_rate = 0.7  # 狩猎成功率
        self.territory_size = 50  # 领地大小(km²)
    
    def make_sound(self) -> str:
        """老鹰的叫声"""
        return f"{self.name}: 啾啾啾! 🦅"
    
    def get_diet_type(self) -> str:
        """老鹰的饮食类型"""
        return "肉食性"
    
    def hunt_prey(self, prey: str) -> str:
        """狩猎"""
        import random
        success = random.random() < self.hunting_success_rate
        if success:
            return f"🎯 {self.name} 成功捕获了 {prey}"
        return f"😔 {self.name} 没有捕获到 {prey}"
    
    def soar(self) -> str:
        """翱翔"""
        return f"🌤️  {self.name} 在高空中优雅地翱翔"


# ==================== 动物园管理系统 ====================
class Zoo:
    """动物园类 - 管理所有动物"""
    
    def __init__(self, name: str):
        """初始化动物园"""
        self.name = name
        self.animals: List[Animal] = []
        self.feeding_schedule: dict = {}
        
        print(f"🏛️  {name} 动物园已开放!")
    
    def add_animal(self, animal: Animal):
        """添加动物"""
        self.animals.append(animal)
        print(f"🎉 {animal} 已加入 {self.name}")
    
    def feed_all_animals(self):
        """喂养所有动物"""
        print(f"\n🍽️  开始喂养时间:")
        for animal in self.animals:
            food = self._get_appropriate_food(animal)
            print(f"   {animal.eat(food)}")
    
    def _get_appropriate_food(self, animal: Animal) -> str:
        """根据动物类型获取合适的食物"""
        diet_type = animal.get_diet_type()
        food_map = {
            "肉食性": "肉类",
            "草食性": "草料和蔬菜",
            "杂食性": "混合饲料"
        }
        return food_map.get(diet_type, "通用饲料")
    
    def animal_show(self):
        """动物表演"""
        print(f"\n🎪 {self.name} 动物表演开始:")
        for animal in self.animals:
            print(f"   {animal.make_sound()}")
            
            # 根据动物类型执行特殊表演
            if isinstance(animal, Dog):
                if animal.tricks_learned:
                    trick = animal.tricks_learned[0]
                    print(f"   {animal.perform_trick(trick)}")
            elif isinstance(animal, Cat):
                print(f"   {animal.purr()}")
            elif isinstance(animal, Elephant):
                print(f"   {animal.spray_water()}")
            elif isinstance(animal, Eagle):
                print(f"   {animal.soar()}")
    
    def get_animals_by_type(self, animal_type: type) -> List[Animal]:
        """根据类型获取动物"""
        return [animal for animal in self.animals if isinstance(animal, animal_type)]
    
    def get_zoo_statistics(self) -> str:
        """获取动物园统计信息"""
        total_animals = len(self.animals)
        if total_animals == 0:
            return "动物园暂无动物"
        
        # 按类型统计
        type_counts = {}
        total_weight = 0
        avg_age = 0
        
        for animal in self.animals:
            animal_type = type(animal).__name__
            type_counts[animal_type] = type_counts.get(animal_type, 0) + 1
            total_weight += animal.weight
            avg_age += animal.age
        
        avg_weight = total_weight / total_animals
        avg_age = avg_age / total_animals
        
        stats = [
            f"📊 {self.name} 统计信息:",
            f"   动物总数: {total_animals}只",
            f"   平均体重: {avg_weight:.1f}kg",
            f"   平均年龄: {avg_age:.1f}岁",
            "",
            "🐾 动物类型分布:"
        ]
        
        for animal_type, count in type_counts.items():
            percentage = count / total_animals * 100
            stats.append(f"   {animal_type}: {count}只 ({percentage:.1f}%)")
        
        return "\n".join(stats)
    
    def list_all_animals(self):
        """列出所有动物"""
        if not self.animals:
            print("🏛️  动物园暂无动物")
            return
        
        print(f"\n📋 {self.name} 动物名单:")
        print("-" * 60)
        
        for i, animal in enumerate(self.animals, 1):
            print(f"{i:2d}. {animal}")
        
        print("-" * 60)


# ==================== 演示函数 ====================
def demo_inheritance():
    """继承机制演示"""
    print("=" * 80)
    print("🐾 面向对象继承机制演示")
    print("=" * 80)
    
    # 创建动物园
    zoo = Zoo("Python野生动物园")
    
    print(f"\n{'='*20} 动物入园 {'='*20}")
    
    # 创建各种动物
    # 狗
    dog = Dog("旺财", 3, 25.5, "金黄色", "金毛")
    dog.learn_trick("坐下")
    dog.learn_trick("握手")
    dog.learn_trick("装死")
    zoo.add_animal(dog)
    
    # 猫
    cat = Cat("咪咪", 2, 4.2, "橘色", True)
    cat.add_favorite_spot("窗台")
    cat.add_favorite_spot("猫爬架")
    zoo.add_animal(cat)
    
    # 大象
    elephant = Elephant("大宝", 15, 4500, 180)
    elephant.remember_friend("小宝")
    elephant.remember_friend("二宝")
    zoo.add_animal(elephant)
    
    # 老鹰
    eagle = Eagle("翱翔", 5, 6.8, 220)
    eagle.build_nest("高山悬崖")
    zoo.add_animal(eagle)
    
    print(f"\n{'='*20} 动物信息展示 {'='*20}")
    
    # 显示动物详细信息
    for animal in zoo.animals[:2]:  # 只显示前两个动物的详细信息
        print(f"\n{animal.get_basic_info()}")
    
    print(f"\n{'='*20} 继承特性演示 {'='*20}")
    
    # 演示继承和多态
    print(f"\n🔊 所有动物发声:")
    for animal in zoo.animals:
        print(f"   {animal.make_sound()}")
    
    print(f"\n🍽️  动物饮食类型:")
    for animal in zoo.animals:
        print(f"   {animal}: {animal.get_diet_type()}")
    
    print(f"\n🎪 特殊技能展示:")
    print(f"   {dog.fetch()}")
    print(f"   {dog.perform_trick('握手')}")
    print(f"   {cat.climb('书架')}")
    print(f"   {cat.hunt()}")
    print(f"   {elephant.use_trunk('拿香蕉')}")
    print(f"   {elephant.trumpet()}")
    print(f"   {eagle.hunt_prey('兔子')}")
    print(f"   {eagle.soar()}")
    
    print(f"\n{'='*20} 类型检查和筛选 {'='*20}")
    
    # 类型检查
    print(f"\n🔍 类型检查:")
    for animal in zoo.animals:
        print(f"   {animal.name} 是否为哺乳动物: {isinstance(animal, Mammal)}")
        print(f"   {animal.name} 是否为鸟类: {isinstance(animal, Bird)}")
    
    # 按类型筛选
    print(f"\n📊 按类型筛选:")
    mammals = zoo.get_animals_by_type(Mammal)
    birds = zoo.get_animals_by_type(Bird)
    print(f"   哺乳动物: {[animal.name for animal in mammals]}")
    print(f"   鸟类: {[animal.name for animal in birds]}")
    
    print(f"\n{'='*20} 动物园活动 {'='*20}")
    
    # 动物园活动
    zoo.feed_all_animals()
    zoo.animal_show()
    
    print(f"\n{'='*20} 统计信息 {'='*20}")
    
    # 统计信息
    print(f"\n{zoo.get_zoo_statistics()}")
    zoo.list_all_animals()
    
    print("\n" + "=" * 80)
    print("🎉 继承机制演示完成!")
    print("💡 关键点:")
    print("   - 继承允许子类复用父类的代码")
    print("   - 方法重写让子类提供特定的实现")
    print("   - super()用于调用父类的方法")
    print("   - isinstance()用于检查对象类型")
    print("   - 抽象基类定义接口规范")
    print("=" * 80)


if __name__ == "__main__":
    demo_inheritance()
