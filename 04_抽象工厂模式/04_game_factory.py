"""
04_game_factory.py - 游戏开发抽象工厂模式

游戏主题系统示例
这个示例展示了如何使用抽象工厂模式来创建不同主题的游戏元素。
在游戏开发中，经常需要支持多种主题（如科幻、魔幻、现代），
抽象工厂模式可以确保同一主题的所有游戏元素风格一致。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum
import random


# ==================== 游戏元素枚举 ====================
class WeaponType(Enum):
    """武器类型"""
    MELEE = "近战"
    RANGED = "远程"
    MAGIC = "魔法"


class EnemyType(Enum):
    """敌人类型"""
    WEAK = "弱敌"
    NORMAL = "普通"
    BOSS = "首领"


# ==================== 抽象产品类 ====================
class Weapon(ABC):
    """武器抽象基类"""
    
    def __init__(self, name: str, damage: int, weapon_type: WeaponType):
        self.name = name
        self.damage = damage
        self.weapon_type = weapon_type
        self.durability = 100
    
    @abstractmethod
    def attack(self) -> str:
        """攻击动作"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取武器描述"""
        pass
    
    def repair(self):
        """修理武器"""
        self.durability = 100


class Enemy(ABC):
    """敌人抽象基类"""
    
    def __init__(self, name: str, health: int, attack_power: int, enemy_type: EnemyType):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.enemy_type = enemy_type
        self.is_alive = True
    
    @abstractmethod
    def attack(self) -> str:
        """攻击动作"""
        pass
    
    @abstractmethod
    def take_damage(self, damage: int) -> str:
        """受到伤害"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取敌人描述"""
        pass


class Environment(ABC):
    """环境抽象基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.weather = "晴朗"
        self.time_of_day = "白天"
    
    @abstractmethod
    def get_ambient_sound(self) -> str:
        """获取环境音效"""
        pass
    
    @abstractmethod
    def get_visual_effect(self) -> str:
        """获取视觉效果"""
        pass
    
    @abstractmethod
    def apply_environment_effect(self, character) -> str:
        """应用环境效果"""
        pass


# ==================== 科幻主题产品族 ====================
class SciFiWeapon(Weapon):
    """科幻武器"""
    
    def __init__(self, name: str, damage: int, weapon_type: WeaponType, energy_cost: int = 10):
        super().__init__(name, damage, weapon_type)
        self.energy_cost = energy_cost
        self.technology_level = random.randint(1, 10)
    
    def attack(self) -> str:
        """科幻武器攻击"""
        effects = ["激光束闪烁", "等离子爆炸", "能量波动", "粒子束发射"]
        effect = random.choice(effects)
        return f"{self.name}发射！{effect}，造成{self.damage}点伤害"
    
    def get_description(self) -> str:
        """获取科幻武器描述"""
        return (f"科幻武器: {self.name} | 伤害: {self.damage} | "
                f"类型: {self.weapon_type.value} | 科技等级: {self.technology_level} | "
                f"能量消耗: {self.energy_cost}")


class SciFiEnemy(Enemy):
    """科幻敌人"""
    
    def __init__(self, name: str, health: int, attack_power: int, enemy_type: EnemyType):
        super().__init__(name, health, attack_power, enemy_type)
        self.shield = random.randint(0, 50)
        self.ai_level = random.randint(1, 5)
    
    def attack(self) -> str:
        """科幻敌人攻击"""
        attacks = ["发射激光", "释放电磁脉冲", "启动导弹", "使用等离子炮"]
        attack = random.choice(attacks)
        return f"{self.name}{attack}，造成{self.attack_power}点伤害"
    
    def take_damage(self, damage: int) -> str:
        """科幻敌人受到伤害"""
        actual_damage = max(0, damage - self.shield)
        self.health -= actual_damage
        
        if self.health <= 0:
            self.is_alive = False
            return f"{self.name}的护盾吸收了{self.shield}点伤害，受到{actual_damage}点伤害后爆炸解体！"
        else:
            return f"{self.name}的护盾吸收了{self.shield}点伤害，受到{actual_damage}点伤害，剩余生命值: {self.health}"
    
    def get_description(self) -> str:
        """获取科幻敌人描述"""
        return (f"科幻敌人: {self.name} | 生命值: {self.health}/{self.max_health} | "
                f"攻击力: {self.attack_power} | 护盾: {self.shield} | AI等级: {self.ai_level}")


class SciFiEnvironment(Environment):
    """科幻环境"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.radiation_level = random.randint(0, 100)
        self.gravity = random.uniform(0.5, 2.0)
    
    def get_ambient_sound(self) -> str:
        """获取科幻环境音效"""
        sounds = ["机械嗡鸣声", "电子音乐", "引擎轰鸣", "警报声", "静电噪音"]
        return f"环境音效: {random.choice(sounds)}"
    
    def get_visual_effect(self) -> str:
        """获取科幻视觉效果"""
        effects = ["霓虹灯闪烁", "全息投影", "粒子特效", "激光网格", "能量场波动"]
        return f"视觉效果: {random.choice(effects)}"
    
    def apply_environment_effect(self, character) -> str:
        """应用科幻环境效果"""
        if self.radiation_level > 70:
            return f"高辐射环境！{character}受到辐射伤害"
        elif self.gravity > 1.5:
            return f"高重力环境！{character}移动速度降低"
        elif self.gravity < 0.8:
            return f"低重力环境！{character}跳跃能力增强"
        else:
            return f"环境正常，{character}状态良好"


# ==================== 魔幻主题产品族 ====================
class FantasyWeapon(Weapon):
    """魔幻武器"""
    
    def __init__(self, name: str, damage: int, weapon_type: WeaponType, magic_power: int = 0):
        super().__init__(name, damage, weapon_type)
        self.magic_power = magic_power
        self.enchantment = random.choice(["火焰", "冰霜", "雷电", "神圣", "暗影", "无"])
    
    def attack(self) -> str:
        """魔幻武器攻击"""
        if self.enchantment != "无":
            return f"{self.name}挥舞！{self.enchantment}能量爆发，造成{self.damage + self.magic_power}点伤害"
        else:
            return f"{self.name}挥舞！造成{self.damage}点物理伤害"
    
    def get_description(self) -> str:
        """获取魔幻武器描述"""
        return (f"魔幻武器: {self.name} | 伤害: {self.damage} | "
                f"类型: {self.weapon_type.value} | 魔法力量: {self.magic_power} | "
                f"附魔: {self.enchantment}")


class FantasyEnemy(Enemy):
    """魔幻敌人"""
    
    def __init__(self, name: str, health: int, attack_power: int, enemy_type: EnemyType):
        super().__init__(name, health, attack_power, enemy_type)
        self.mana = random.randint(20, 100)
        self.magic_resistance = random.randint(0, 30)
    
    def attack(self) -> str:
        """魔幻敌人攻击"""
        if self.mana >= 20:
            attacks = ["施放火球术", "召唤闪电", "释放冰锥", "使用治疗术"]
            attack = random.choice(attacks)
            self.mana -= 20
            return f"{self.name}{attack}，造成{self.attack_power + 10}点魔法伤害"
        else:
            attacks = ["挥爪攻击", "撕咬", "冲撞", "尾击"]
            attack = random.choice(attacks)
            return f"{self.name}{attack}，造成{self.attack_power}点物理伤害"
    
    def take_damage(self, damage: int) -> str:
        """魔幻敌人受到伤害"""
        actual_damage = max(0, damage - self.magic_resistance)
        self.health -= actual_damage
        
        if self.health <= 0:
            self.is_alive = False
            return f"{self.name}的魔法抗性减少了{self.magic_resistance}点伤害，受到{actual_damage}点伤害后倒下！"
        else:
            return f"{self.name}的魔法抗性减少了{self.magic_resistance}点伤害，受到{actual_damage}点伤害，剩余生命值: {self.health}"
    
    def get_description(self) -> str:
        """获取魔幻敌人描述"""
        return (f"魔幻敌人: {self.name} | 生命值: {self.health}/{self.max_health} | "
                f"攻击力: {self.attack_power} | 法力值: {self.mana} | 魔法抗性: {self.magic_resistance}")


class FantasyEnvironment(Environment):
    """魔幻环境"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.magic_density = random.randint(0, 100)
        self.mystical_creatures = random.choice([True, False])
    
    def get_ambient_sound(self) -> str:
        """获取魔幻环境音效"""
        sounds = ["神秘咒语声", "魔法能量嗡鸣", "远古钟声", "精灵歌声", "龙吟声"]
        return f"环境音效: {random.choice(sounds)}"
    
    def get_visual_effect(self) -> str:
        """获取魔幻视觉效果"""
        effects = ["魔法光芒", "浮动符文", "星光闪烁", "魔法粒子", "神秘雾气"]
        return f"视觉效果: {random.choice(effects)}"
    
    def apply_environment_effect(self, character) -> str:
        """应用魔幻环境效果"""
        if self.magic_density > 70:
            return f"高魔法密度环境！{character}的魔法能力增强"
        elif self.mystical_creatures:
            return f"神秘生物出没！{character}感受到古老的力量"
        else:
            return f"平静的魔法环境，{character}感到安宁"


# ==================== 抽象工厂类 ====================
class GameFactory(ABC):
    """游戏元素抽象工厂"""
    
    @abstractmethod
    def create_weapon(self, weapon_type: WeaponType) -> Weapon:
        """创建武器"""
        pass
    
    @abstractmethod
    def create_enemy(self, enemy_type: EnemyType) -> Enemy:
        """创建敌人"""
        pass
    
    @abstractmethod
    def create_environment(self, env_name: str) -> Environment:
        """创建环境"""
        pass


# ==================== 具体工厂类 ====================
class SciFiGameFactory(GameFactory):
    """科幻游戏工厂"""
    
    def create_weapon(self, weapon_type: WeaponType) -> Weapon:
        """创建科幻武器"""
        weapons = {
            WeaponType.MELEE: [
                ("光剑", 80, 15),
                ("等离子刀", 70, 12),
                ("能量战锤", 90, 20)
            ],
            WeaponType.RANGED: [
                ("激光步枪", 60, 8),
                ("粒子炮", 100, 25),
                ("电磁狙击枪", 120, 30)
            ],
            WeaponType.MAGIC: [
                ("纳米治疗器", 30, 5),
                ("心灵控制器", 50, 15),
                ("时空扭曲器", 150, 50)
            ]
        }
        
        name, damage, energy_cost = random.choice(weapons[weapon_type])
        return SciFiWeapon(name, damage, weapon_type, energy_cost)
    
    def create_enemy(self, enemy_type: EnemyType) -> Enemy:
        """创建科幻敌人"""
        enemies = {
            EnemyType.WEAK: [
                ("侦察机器人", 50, 15),
                ("无人机", 40, 12),
                ("安保机器人", 60, 18)
            ],
            EnemyType.NORMAL: [
                ("战斗机器人", 120, 35),
                ("外星战士", 100, 30),
                ("赛博格士兵", 110, 32)
            ],
            EnemyType.BOSS: [
                ("机械巨龙", 500, 80),
                ("外星母舰", 600, 90),
                ("AI核心", 400, 70)
            ]
        }
        
        name, health, attack_power = random.choice(enemies[enemy_type])
        return SciFiEnemy(name, health, attack_power, enemy_type)
    
    def create_environment(self, env_name: str) -> Environment:
        """创建科幻环境"""
        environments = {
            "太空站": "一个巨大的太空站，充满了高科技设备和全息显示器",
            "外星基地": "位于遥远星球上的外星人基地，到处都是未知的科技",
            "赛博城市": "未来的城市，霓虹灯闪烁，飞行汽车穿梭其间"
        }
        
        description = environments.get(env_name, "未知的科幻环境")
        return SciFiEnvironment(env_name, description)


class FantasyGameFactory(GameFactory):
    """魔幻游戏工厂"""
    
    def create_weapon(self, weapon_type: WeaponType) -> Weapon:
        """创建魔幻武器"""
        weapons = {
            WeaponType.MELEE: [
                ("龙鳞剑", 75, 20),
                ("秘银战锤", 85, 15),
                ("精灵长弓", 65, 25)
            ],
            WeaponType.RANGED: [
                ("魔法弩", 55, 18),
                ("符文投矛", 70, 22),
                ("精灵长弓", 60, 20)
            ],
            WeaponType.MAGIC: [
                ("法师法杖", 40, 40),
                ("治疗权杖", 25, 35),
                ("毁灭法杖", 100, 60)
            ]
        }
        
        name, damage, magic_power = random.choice(weapons[weapon_type])
        return FantasyWeapon(name, damage, weapon_type, magic_power)
    
    def create_enemy(self, enemy_type: EnemyType) -> Enemy:
        """创建魔幻敌人"""
        enemies = {
            EnemyType.WEAK: [
                ("哥布林", 45, 12),
                ("骷髅兵", 40, 10),
                ("野狼", 35, 15)
            ],
            EnemyType.NORMAL: [
                ("兽人战士", 100, 28),
                ("暗黑法师", 80, 35),
                ("石头巨人", 150, 25)
            ],
            EnemyType.BOSS: [
                ("古龙", 800, 100),
                ("巫妖王", 600, 120),
                ("恶魔领主", 700, 110)
            ]
        }
        
        name, health, attack_power = random.choice(enemies[enemy_type])
        return FantasyEnemy(name, health, attack_power, enemy_type)
    
    def create_environment(self, env_name: str) -> Environment:
        """创建魔幻环境"""
        environments = {
            "魔法森林": "古老的森林，树木高耸入云，魔法能量在空气中流淌",
            "龙穴": "巨龙的巢穴，到处都是宝藏和危险的魔法陷阱",
            "魔法塔": "高耸的法师塔，每一层都充满了神秘的魔法实验"
        }
        
        description = environments.get(env_name, "未知的魔幻环境")
        return FantasyEnvironment(env_name, description)


# ==================== 游戏管理器 ====================
class GameManager:
    """游戏管理器"""
    
    def __init__(self, factory: GameFactory):
        self.factory = factory
        self.player_weapons = []
        self.current_enemies = []
        self.current_environment = None
    
    def setup_game_scene(self, env_name: str):
        """设置游戏场景"""
        print(f"正在设置游戏场景: {env_name}")
        
        # 创建环境
        self.current_environment = self.factory.create_environment(env_name)
        print(f"环境: {self.current_environment.name}")
        print(f"描述: {self.current_environment.description}")
        print(self.current_environment.get_ambient_sound())
        print(self.current_environment.get_visual_effect())
        
        # 创建武器
        weapon_types = [WeaponType.MELEE, WeaponType.RANGED, WeaponType.MAGIC]
        for weapon_type in weapon_types:
            weapon = self.factory.create_weapon(weapon_type)
            self.player_weapons.append(weapon)
            print(f"获得武器: {weapon.get_description()}")
        
        # 创建敌人
        enemy_types = [EnemyType.WEAK, EnemyType.NORMAL, EnemyType.BOSS]
        for enemy_type in enemy_types:
            enemy = self.factory.create_enemy(enemy_type)
            self.current_enemies.append(enemy)
            print(f"遭遇敌人: {enemy.get_description()}")
    
    def simulate_battle(self):
        """模拟战斗"""
        print("\n开始战斗模拟!")
        
        for i, weapon in enumerate(self.player_weapons):
            if i < len(self.current_enemies) and self.current_enemies[i].is_alive:
                enemy = self.current_enemies[i]
                
                print(f"\n使用 {weapon.name} 攻击 {enemy.name}:")
                attack_result = weapon.attack()
                print(attack_result)
                
                damage_result = enemy.take_damage(weapon.damage)
                print(damage_result)
                
                if enemy.is_alive:
                    counter_attack = enemy.attack()
                    print(f"反击: {counter_attack}")
        
        # 应用环境效果
        if self.current_environment:
            env_effect = self.current_environment.apply_environment_effect("玩家")
            print(f"\n环境效果: {env_effect}")


# ==================== 演示函数 ====================
def demonstrate_scifi_game():
    """演示科幻游戏"""
    print("=" * 60)
    print("科幻主题游戏演示")
    print("=" * 60)
    
    # 创建科幻游戏工厂
    scifi_factory = SciFiGameFactory()
    
    # 创建游戏管理器
    game_manager = GameManager(scifi_factory)
    
    # 设置游戏场景
    game_manager.setup_game_scene("太空站")
    
    # 模拟战斗
    game_manager.simulate_battle()


def demonstrate_fantasy_game():
    """演示魔幻游戏"""
    print("\n" + "=" * 60)
    print("魔幻主题游戏演示")
    print("=" * 60)
    
    # 创建魔幻游戏工厂
    fantasy_factory = FantasyGameFactory()
    
    # 创建游戏管理器
    game_manager = GameManager(fantasy_factory)
    
    # 设置游戏场景
    game_manager.setup_game_scene("魔法森林")
    
    # 模拟战斗
    game_manager.simulate_battle()


def main():
    """主函数"""
    print("抽象工厂模式演示 - 游戏主题系统")
    
    demonstrate_scifi_game()
    demonstrate_fantasy_game()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
