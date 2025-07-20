"""
01_basic_prototype.py - 原型模式基础实现

游戏角色系统示例
这个示例展示了如何使用原型模式来创建游戏角色。
在游戏开发中，经常需要创建大量相似的角色对象，
原型模式可以避免重复的初始化工作，提高性能。
"""

import copy
from abc import ABC, abstractmethod
from typing import Dict, List


# ==================== 原型接口 ====================
class GameCharacterPrototype(ABC):
    """游戏角色原型抽象基类"""
    
    @abstractmethod
    def clone(self):
        """克隆方法 - 创建当前对象的副本"""
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        """获取角色信息"""
        pass


# ==================== 具体原型类 ====================
class Warrior(GameCharacterPrototype):
    """战士角色类"""
    
    def __init__(self, name: str = "无名战士"):
        self.name = name
        self.character_type = "战士"
        self.level = 1
        self.health = 100
        self.attack = 20
        self.defense = 15
        self.skills = ["重击", "格挡"]
        self.equipment = {
            "weapon": "铁剑",
            "armor": "皮甲",
            "shield": "木盾"
        }
        self.experience = 0
    
    def clone(self):
        """克隆战士角色"""
        # 使用浅拷贝创建新的战士对象
        new_warrior = copy.copy(self)
        # 为可变属性创建新的副本，避免共享引用
        new_warrior.skills = self.skills.copy()
        new_warrior.equipment = self.equipment.copy()
        return new_warrior
    
    def deep_clone(self):
        """深度克隆战士角色"""
        return copy.deepcopy(self)
    
    def level_up(self):
        """升级"""
        self.level += 1
        self.health += 10
        self.attack += 3
        self.defense += 2
        self.experience = 0
        print(f"{self.name} 升级到 {self.level} 级！")
    
    def add_experience(self, exp: int):
        """增加经验值"""
        self.experience += exp
        if self.experience >= 100:
            self.level_up()
    
    def equip_weapon(self, weapon: str):
        """装备武器"""
        old_weapon = self.equipment["weapon"]
        self.equipment["weapon"] = weapon
        print(f"{self.name} 将 {old_weapon} 替换为 {weapon}")
    
    def get_info(self) -> str:
        """获取角色信息"""
        return (f"角色: {self.name} ({self.character_type})\n"
                f"等级: {self.level} | 生命值: {self.health}\n"
                f"攻击力: {self.attack} | 防御力: {self.defense}\n"
                f"技能: {', '.join(self.skills)}\n"
                f"装备: {self.equipment}")


class Mage(GameCharacterPrototype):
    """法师角色类"""
    
    def __init__(self, name: str = "无名法师"):
        self.name = name
        self.character_type = "法师"
        self.level = 1
        self.health = 70
        self.mana = 100
        self.magic_power = 25
        self.defense = 8
        self.spells = ["火球术", "治疗术"]
        self.equipment = {
            "weapon": "法杖",
            "robe": "布袍",
            "accessory": "魔法戒指"
        }
        self.spell_book = []
    
    def clone(self):
        """克隆法师角色"""
        new_mage = copy.copy(self)
        new_mage.spells = self.spells.copy()
        new_mage.equipment = self.equipment.copy()
        new_mage.spell_book = self.spell_book.copy()
        return new_mage
    
    def deep_clone(self):
        """深度克隆法师角色"""
        return copy.deepcopy(self)
    
    def learn_spell(self, spell: str):
        """学习新法术"""
        if spell not in self.spells:
            self.spells.append(spell)
            self.spell_book.append(f"学会了 {spell}")
            print(f"{self.name} 学会了 {spell}！")
    
    def cast_spell(self, spell: str, target: str = "敌人"):
        """施放法术"""
        if spell in self.spells and self.mana >= 10:
            self.mana -= 10
            print(f"{self.name} 对 {target} 施放了 {spell}！")
            return True
        else:
            print(f"{self.name} 无法施放 {spell}（法力不足或未学会）")
            return False
    
    def get_info(self) -> str:
        """获取角色信息"""
        return (f"角色: {self.name} ({self.character_type})\n"
                f"等级: {self.level} | 生命值: {self.health} | 法力值: {self.mana}\n"
                f"魔法攻击力: {self.magic_power} | 防御力: {self.defense}\n"
                f"法术: {', '.join(self.spells)}\n"
                f"装备: {self.equipment}")


class Archer(GameCharacterPrototype):
    """弓箭手角色类"""
    
    def __init__(self, name: str = "无名弓箭手"):
        self.name = name
        self.character_type = "弓箭手"
        self.level = 1
        self.health = 85
        self.attack = 18
        self.accuracy = 90  # 命中率
        self.defense = 10
        self.skills = ["精准射击", "多重射击"]
        self.equipment = {
            "weapon": "短弓",
            "armor": "皮甲",
            "quiver": "箭袋"
        }
        self.arrows = 50
    
    def clone(self):
        """克隆弓箭手角色"""
        new_archer = copy.copy(self)
        new_archer.skills = self.skills.copy()
        new_archer.equipment = self.equipment.copy()
        return new_archer
    
    def deep_clone(self):
        """深度克隆弓箭手角色"""
        return copy.deepcopy(self)
    
    def shoot_arrow(self, target: str = "敌人"):
        """射箭"""
        if self.arrows > 0:
            self.arrows -= 1
            print(f"{self.name} 向 {target} 射出一箭！剩余箭矢: {self.arrows}")
            return True
        else:
            print(f"{self.name} 没有箭矢了！")
            return False
    
    def refill_arrows(self, count: int = 30):
        """补充箭矢"""
        self.arrows += count
        print(f"{self.name} 补充了 {count} 支箭矢，当前箭矢: {self.arrows}")
    
    def get_info(self) -> str:
        """获取角色信息"""
        return (f"角色: {self.name} ({self.character_type})\n"
                f"等级: {self.level} | 生命值: {self.health}\n"
                f"攻击力: {self.attack} | 命中率: {self.accuracy}% | 防御力: {self.defense}\n"
                f"技能: {', '.join(self.skills)}\n"
                f"箭矢数量: {self.arrows}\n"
                f"装备: {self.equipment}")


# ==================== 原型管理器 ====================
class CharacterPrototypeManager:
    """角色原型管理器"""
    
    def __init__(self):
        self._prototypes: Dict[str, GameCharacterPrototype] = {}
        self._initialize_default_prototypes()
    
    def _initialize_default_prototypes(self):
        """初始化默认原型"""
        # 创建默认的角色原型
        default_warrior = Warrior("战士模板")
        default_mage = Mage("法师模板")
        default_archer = Archer("弓箭手模板")
        
        # 注册原型
        self.register_prototype("warrior", default_warrior)
        self.register_prototype("mage", default_mage)
        self.register_prototype("archer", default_archer)
        
        # 创建一些预配置的高级原型
        elite_warrior = Warrior("精英战士模板")
        elite_warrior.level = 5
        elite_warrior.health = 150
        elite_warrior.attack = 35
        elite_warrior.defense = 25
        elite_warrior.skills.extend(["狂暴", "战吼"])
        elite_warrior.equipment["weapon"] = "钢剑"
        elite_warrior.equipment["armor"] = "链甲"
        
        self.register_prototype("elite_warrior", elite_warrior)
    
    def register_prototype(self, name: str, prototype: GameCharacterPrototype):
        """注册原型"""
        self._prototypes[name] = prototype
        print(f"原型管理器: 已注册原型 '{name}'")
    
    def unregister_prototype(self, name: str):
        """注销原型"""
        if name in self._prototypes:
            del self._prototypes[name]
            print(f"原型管理器: 已注销原型 '{name}'")
        else:
            print(f"原型管理器: 未找到原型 '{name}'")
    
    def create_character(self, prototype_name: str, character_name: str = None) -> GameCharacterPrototype:
        """根据原型创建角色"""
        if prototype_name not in self._prototypes:
            raise ValueError(f"未找到名为 '{prototype_name}' 的原型")
        
        # 克隆原型
        new_character = self._prototypes[prototype_name].clone()
        
        # 如果提供了角色名称，则设置新名称
        if character_name:
            new_character.name = character_name
        
        print(f"原型管理器: 基于 '{prototype_name}' 创建了角色 '{new_character.name}'")
        return new_character
    
    def list_prototypes(self) -> List[str]:
        """列出所有可用的原型"""
        return list(self._prototypes.keys())
    
    def get_prototype_info(self, name: str) -> str:
        """获取原型信息"""
        if name in self._prototypes:
            return self._prototypes[name].get_info()
        else:
            return f"未找到原型 '{name}'"


# ==================== 演示函数 ====================
def demonstrate_basic_cloning():
    """演示基础克隆功能"""
    print("=" * 50)
    print("基础克隆演示")
    print("=" * 50)
    
    # 创建原始战士
    original_warrior = Warrior("亚瑟")
    original_warrior.level = 3
    original_warrior.add_experience(50)
    original_warrior.equip_weapon("魔法剑")
    
    print("原始战士信息:")
    print(original_warrior.get_info())
    print()
    
    # 克隆战士
    cloned_warrior = original_warrior.clone()
    cloned_warrior.name = "兰斯洛特"
    
    print("克隆战士信息:")
    print(cloned_warrior.get_info())
    print()
    
    # 修改原始战士，观察克隆对象是否受影响
    print("修改原始战士的技能...")
    original_warrior.skills.append("旋风斩")
    
    print("修改后的原始战士技能:", original_warrior.skills)
    print("克隆战士的技能:", cloned_warrior.skills)
    print("注意: 由于使用了浅拷贝并正确处理了可变属性，克隆对象不受影响")


def demonstrate_prototype_manager():
    """演示原型管理器的使用"""
    print("\n" + "=" * 50)
    print("原型管理器演示")
    print("=" * 50)
    
    # 创建原型管理器
    manager = CharacterPrototypeManager()
    
    # 列出可用原型
    print("可用的原型:")
    for prototype_name in manager.list_prototypes():
        print(f"- {prototype_name}")
    print()
    
    # 创建角色
    print("创建角色:")
    hero1 = manager.create_character("warrior", "勇者小明")
    hero2 = manager.create_character("mage", "智者小红")
    hero3 = manager.create_character("elite_warrior", "精英小强")
    print()
    
    # 显示创建的角色信息
    characters = [hero1, hero2, hero3]
    for i, character in enumerate(characters, 1):
        print(f"角色 {i}:")
        print(character.get_info())
        print("-" * 30)


def demonstrate_deep_vs_shallow_copy():
    """演示深拷贝与浅拷贝的区别"""
    print("\n" + "=" * 50)
    print("深拷贝 vs 浅拷贝演示")
    print("=" * 50)
    
    # 创建原始法师
    original_mage = Mage("甘道夫")
    original_mage.learn_spell("闪电术")
    original_mage.spell_book.append("古老的咒语书")
    
    print("原始法师信息:")
    print(f"法术: {original_mage.spells}")
    print(f"法术书: {original_mage.spell_book}")
    print()
    
    # 浅拷贝
    shallow_copy_mage = original_mage.clone()
    shallow_copy_mage.name = "萨鲁曼"
    
    # 深拷贝
    deep_copy_mage = original_mage.deep_clone()
    deep_copy_mage.name = "拉达加斯特"
    
    print("修改原始法师的法术书...")
    original_mage.spell_book.append("禁忌法术")
    
    print(f"原始法师法术书: {original_mage.spell_book}")
    print(f"浅拷贝法师法术书: {shallow_copy_mage.spell_book}")
    print(f"深拷贝法师法术书: {deep_copy_mage.spell_book}")
    print()
    print("注意: 浅拷贝正确处理了可变属性，所以不会受到影响")
    print("深拷贝创建了完全独立的副本")


# ==================== 主函数 ====================
def main():
    """主函数 - 演示原型模式的各种用法"""
    print("原型模式演示 - 游戏角色系统")
    
    # 演示基础克隆
    demonstrate_basic_cloning()
    
    # 演示原型管理器
    demonstrate_prototype_manager()
    
    # 演示深拷贝与浅拷贝
    demonstrate_deep_vs_shallow_copy()
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
