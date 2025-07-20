"""
04_game_character.py - 游戏角色状态系统

这个示例展示了游戏开发中的状态模式应用。
演示了角色的多种状态、状态影响的行为变化、状态间的复杂交互。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
import time


# ==================== 枚举定义 ====================

class SkillType(Enum):
    """技能类型"""
    ATTACK = "attack"
    DEFENSE = "defense"
    HEAL = "heal"
    BUFF = "buff"
    DEBUFF = "debuff"


class DamageType(Enum):
    """伤害类型"""
    PHYSICAL = "physical"
    MAGICAL = "magical"
    TRUE = "true"


# ==================== 抽象状态接口 ====================

class CharacterState(ABC):
    """角色状态抽象类"""

    @abstractmethod
    def get_state_name(self) -> str:
        """获取状态名称"""
        pass

    @abstractmethod
    def get_state_icon(self) -> str:
        """获取状态图标"""
        pass

    @abstractmethod
    def can_attack(self) -> bool:
        """是否可以攻击"""
        pass

    @abstractmethod
    def can_move(self) -> bool:
        """是否可以移动"""
        pass

    @abstractmethod
    def can_use_skill(self, skill_type: SkillType) -> bool:
        """是否可以使用技能"""
        pass

    @abstractmethod
    def get_damage_multiplier(self, damage_type: DamageType) -> float:
        """获取伤害倍率"""
        pass

    @abstractmethod
    def get_speed_multiplier(self) -> float:
        """获取速度倍率"""
        pass

    @abstractmethod
    def on_enter(self, character: 'GameCharacter') -> None:
        """进入状态时的处理"""
        pass

    @abstractmethod
    def on_exit(self, character: 'GameCharacter') -> None:
        """离开状态时的处理"""
        pass

    @abstractmethod
    def on_update(self, character: 'GameCharacter', delta_time: float) -> None:
        """状态更新（每帧调用）"""
        pass


# ==================== 游戏角色类 ====================

class GameCharacter:
    """游戏角色类"""

    def __init__(self, name: str, character_class: str = "战士"):
        self.name = name
        self.character_class = character_class

        # 基础属性
        self.max_health = 100
        self.max_mana = 50
        self.max_stamina = 100

        # 当前属性
        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina

        # 战斗属性
        self.attack_power = 20
        self.defense = 10
        self.speed = 10

        # 状态管理
        self._state: CharacterState = NormalState()
        self._state_duration = 0.0
        self._state_effects: Dict[str, float] = {}
        self._pending_tired_state = False

        # 技能冷却
        self._skill_cooldowns: Dict[str, float] = {}

        # 战斗记录
        self._combat_log: List[str] = []

        print(f"⚔️ {self.character_class} {self.name} 进入游戏")
        self._state.on_enter(self)

    def set_state(self, new_state: CharacterState, duration: float = 0.0) -> None:
        """设置新状态"""
        old_state = self._state

        # 防止递归调用
        if hasattr(self, '_state_changing') and self._state_changing:
            return

        self._state_changing = True

        try:
            # 离开旧状态
            old_state.on_exit(self)

            # 进入新状态
            self._state = new_state
            self._state_duration = duration

            print(f"🔄 {self.name}: {old_state.get_state_name()} → {new_state.get_state_name()}")

            # 进入新状态的处理
            new_state.on_enter(self)

        finally:
            self._state_changing = False

            # 处理延迟的状态转换（避免递归）
            if hasattr(self, '_pending_tired_state') and self._pending_tired_state:
                self._pending_tired_state = False
                if not isinstance(new_state, TiredState):  # 避免重复设置
                    self.set_state(TiredState(), 3.0)

    @property
    def current_state(self) -> CharacterState:
        return self._state

    @property
    def state_name(self) -> str:
        return self._state.get_state_name()

    @property
    def state_icon(self) -> str:
        return self._state.get_state_icon()

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def update(self, delta_time: float) -> None:
        """更新角色状态（游戏主循环调用）"""
        # 更新状态持续时间
        if self._state_duration > 0:
            self._state_duration -= delta_time
            if self._state_duration <= 0:
                # 状态时间结束，回到正常状态
                if not isinstance(self._state, (NormalState, DeadState)):
                    self.set_state(NormalState())

        # 更新技能冷却
        for skill in list(self._skill_cooldowns.keys()):
            self._skill_cooldowns[skill] -= delta_time
            if self._skill_cooldowns[skill] <= 0:
                del self._skill_cooldowns[skill]

        # 状态更新
        self._state.on_update(self, delta_time)

        # 自然恢复
        self._natural_recovery(delta_time)

    def _natural_recovery(self, delta_time: float) -> None:
        """自然恢复"""
        if isinstance(self._state, NormalState):
            # 正常状态下缓慢恢复
            self.mana = min(self.max_mana, self.mana + 2 * delta_time)
            self.stamina = min(self.max_stamina, self.stamina + 5 * delta_time)

    def take_damage(self, damage: int, damage_type: DamageType = DamageType.PHYSICAL) -> int:
        """受到伤害"""
        if not self.is_alive:
            return 0

        # 应用状态伤害倍率
        multiplier = self._state.get_damage_multiplier(damage_type)
        actual_damage = int(damage * multiplier)

        # 应用防御
        if damage_type != DamageType.TRUE:
            actual_damage = max(1, actual_damage - self.defense)

        self.health = max(0, self.health - actual_damage)

        self._log(f"受到 {actual_damage} 点{damage_type.value}伤害")

        # 检查死亡
        if self.health <= 0:
            self.set_state(DeadState())
        elif self.health <= self.max_health * 0.2:
            # 生命值低于20%时进入虚弱状态
            if not isinstance(self._state, (WeakState, DeadState)):
                self.set_state(WeakState(), 10.0)

        return actual_damage

    def heal(self, amount: int) -> int:
        """治疗"""
        if not self.is_alive:
            return 0

        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        actual_heal = self.health - old_health

        if actual_heal > 0:
            self._log(f"恢复 {actual_heal} 点生命值")

            # 如果从虚弱状态恢复到安全血量
            if isinstance(self._state, WeakState) and self.health > self.max_health * 0.3:
                self.set_state(NormalState())

        return actual_heal

    def attack(self, target: 'GameCharacter') -> bool:
        """攻击目标"""
        if not self._state.can_attack():
            self._log("当前状态无法攻击")
            return False

        if self.stamina < 10:
            self._log("体力不足，无法攻击")
            return False

        # 消耗体力
        self.stamina -= 10

        # 计算伤害
        base_damage = self.attack_power
        damage = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))

        # 应用状态修正
        if isinstance(self._state, BerserkState):
            damage = int(damage * 1.5)
        elif isinstance(self._state, WeakState):
            damage = int(damage * 0.7)

        actual_damage = target.take_damage(damage)
        self._log(f"攻击 {target.name}，造成 {actual_damage} 点伤害")

        # 攻击后可能触发状态变化
        if self.stamina <= 20:
            self.set_state(TiredState(), 5.0)

        return True

    def use_skill(self, skill_name: str, skill_type: SkillType, target: Optional['GameCharacter'] = None) -> bool:
        """使用技能"""
        if not self._state.can_use_skill(skill_type):
            self._log(f"当前状态无法使用{skill_type.value}技能")
            return False

        if skill_name in self._skill_cooldowns:
            remaining = self._skill_cooldowns[skill_name]
            self._log(f"技能 {skill_name} 冷却中，剩余 {remaining:.1f} 秒")
            return False

        # 技能效果
        success = self._execute_skill(skill_name, skill_type, target)

        if success:
            # 设置冷却时间
            self._skill_cooldowns[skill_name] = 3.0
            self._log(f"使用技能: {skill_name}")

        return success

    def _execute_skill(self, skill_name: str, skill_type: SkillType, target: Optional['GameCharacter']) -> bool:
        """执行技能效果"""
        if skill_type == SkillType.ATTACK:
            if not target or not target.is_alive:
                return False

            if self.mana < 15:
                self._log("法力不足")
                return False

            self.mana -= 15
            damage = int(self.attack_power * 1.8)
            target.take_damage(damage, DamageType.MAGICAL)
            return True

        elif skill_type == SkillType.HEAL:
            if self.mana < 20:
                self._log("法力不足")
                return False

            self.mana -= 20
            heal_amount = random.randint(25, 35)
            self.heal(heal_amount)
            return True

        elif skill_type == SkillType.BUFF:
            if self.mana < 25:
                self._log("法力不足")
                return False

            self.mana -= 25
            if skill_name == "狂暴":
                self.set_state(BerserkState(), 8.0)
            elif skill_name == "防御姿态":
                self.set_state(DefendingState(), 6.0)
            return True

        return False

    def rest(self) -> None:
        """休息"""
        if isinstance(self._state, TiredState):
            self.set_state(NormalState())

        # 恢复体力和法力
        self.stamina = min(self.max_stamina, self.stamina + 30)
        self.mana = min(self.max_mana, self.mana + 20)
        self._log("休息恢复体力和法力")

    def _log(self, message: str) -> None:
        """记录战斗日志"""
        log_entry = f"[{self.name}] {message}"
        self._combat_log.append(log_entry)
        print(f"📝 {log_entry}")

    def get_status(self) -> Dict[str, any]:
        """获取角色状态"""
        return {
            'name': self.name,
            'class': self.character_class,
            'health': f"{self.health}/{self.max_health}",
            'mana': f"{self.mana:.0f}/{self.max_mana}",
            'stamina': f"{self.stamina:.0f}/{self.max_stamina}",
            'state': f"{self.state_icon} {self.state_name}",
            'is_alive': self.is_alive
        }


# ==================== 具体状态类 ====================

class NormalState(CharacterState):
    """正常状态"""

    def get_state_name(self) -> str:
        return "正常"

    def get_state_icon(self) -> str:
        return "😊"

    def can_attack(self) -> bool:
        return True

    def can_move(self) -> bool:
        return True

    def can_use_skill(self, skill_type: SkillType) -> bool:
        return True

    def get_damage_multiplier(self, damage_type: DamageType) -> float:
        return 1.0

    def get_speed_multiplier(self) -> float:
        return 1.0

    def on_enter(self, character: GameCharacter) -> None:
        pass

    def on_exit(self, character: GameCharacter) -> None:
        pass

    def on_update(self, character: GameCharacter, delta_time: float) -> None:
        pass


class WeakState(CharacterState):
    """虚弱状态"""

    def get_state_name(self) -> str:
        return "虚弱"

    def get_state_icon(self) -> str:
        return "😰"

    def can_attack(self) -> bool:
        return True

    def can_move(self) -> bool:
        return True

    def can_use_skill(self, skill_type: SkillType) -> bool:
        return skill_type in [SkillType.HEAL, SkillType.DEFENSE]

    def get_damage_multiplier(self, damage_type: DamageType) -> float:
        return 1.3  # 受到更多伤害

    def get_speed_multiplier(self) -> float:
        return 0.7

    def on_enter(self, character: GameCharacter) -> None:
        character._log("进入虚弱状态，攻击力和移动速度下降")

    def on_exit(self, character: GameCharacter) -> None:
        character._log("脱离虚弱状态")

    def on_update(self, character: GameCharacter, delta_time: float) -> None:
        # 虚弱状态下缓慢失血
        if random.random() < 0.1 * delta_time:
            character.health = max(1, character.health - 1)


class TiredState(CharacterState):
    """疲劳状态"""

    def get_state_name(self) -> str:
        return "疲劳"

    def get_state_icon(self) -> str:
        return "😴"

    def can_attack(self) -> bool:
        return False

    def can_move(self) -> bool:
        return True

    def can_use_skill(self, skill_type: SkillType) -> bool:
        return skill_type == SkillType.HEAL

    def get_damage_multiplier(self, damage_type: DamageType) -> float:
        return 1.2

    def get_speed_multiplier(self) -> float:
        return 0.5

    def on_enter(self, character: GameCharacter) -> None:
        character._log("体力耗尽，进入疲劳状态")

    def on_exit(self, character: GameCharacter) -> None:
        character._log("恢复体力，脱离疲劳状态")

    def on_update(self, character: GameCharacter, delta_time: float) -> None:
        # 疲劳状态下快速恢复体力
        character.stamina = min(character.max_stamina, character.stamina + 10 * delta_time)


class BerserkState(CharacterState):
    """狂暴状态"""

    def get_state_name(self) -> str:
        return "狂暴"

    def get_state_icon(self) -> str:
        return "😡"

    def can_attack(self) -> bool:
        return True

    def can_move(self) -> bool:
        return True

    def can_use_skill(self, skill_type: SkillType) -> bool:
        return skill_type == SkillType.ATTACK

    def get_damage_multiplier(self, damage_type: DamageType) -> float:
        return 1.5  # 受到更多伤害

    def get_speed_multiplier(self) -> float:
        return 1.3

    def on_enter(self, character: GameCharacter) -> None:
        character._log("进入狂暴状态！攻击力大幅提升")

    def on_exit(self, character: GameCharacter) -> None:
        character._log("狂暴状态结束")
        # 标记需要在状态转换完成后进入疲劳状态
        character._pending_tired_state = True

    def on_update(self, character: GameCharacter, delta_time: float) -> None:
        # 狂暴状态下持续消耗体力
        character.stamina = max(0, character.stamina - 5 * delta_time)


class DefendingState(CharacterState):
    """防御状态"""

    def get_state_name(self) -> str:
        return "防御"

    def get_state_icon(self) -> str:
        return "🛡️"

    def can_attack(self) -> bool:
        return False

    def can_move(self) -> bool:
        return False

    def can_use_skill(self, skill_type: SkillType) -> bool:
        return skill_type in [SkillType.DEFENSE, SkillType.HEAL]

    def get_damage_multiplier(self, damage_type: DamageType) -> float:
        return 0.5  # 受到伤害减半

    def get_speed_multiplier(self) -> float:
        return 0.0

    def on_enter(self, character: GameCharacter) -> None:
        character._log("进入防御姿态，大幅减少受到的伤害")

    def on_exit(self, character: GameCharacter) -> None:
        character._log("解除防御姿态")

    def on_update(self, character: GameCharacter, delta_time: float) -> None:
        pass


class DeadState(CharacterState):
    """死亡状态"""

    def get_state_name(self) -> str:
        return "死亡"

    def get_state_icon(self) -> str:
        return "💀"

    def can_attack(self) -> bool:
        return False

    def can_move(self) -> bool:
        return False

    def can_use_skill(self, skill_type: SkillType) -> bool:
        return False

    def get_damage_multiplier(self, damage_type: DamageType) -> float:
        return 0.0

    def get_speed_multiplier(self) -> float:
        return 0.0

    def on_enter(self, character: GameCharacter) -> None:
        character._log("死亡")

    def on_exit(self, character: GameCharacter) -> None:
        character._log("复活")

    def on_update(self, character: GameCharacter, delta_time: float) -> None:
        pass


# ==================== 演示函数 ====================

def demo_character_states():
    """角色状态演示"""
    print("=" * 60)
    print("⚔️ 游戏角色状态系统演示")
    print("=" * 60)

    # 创建角色
    warrior = GameCharacter("亚瑟", "战士")
    mage = GameCharacter("梅林", "法师")

    print(f"\n📊 初始状态:")
    print(f"   {warrior.get_status()}")
    print(f"   {mage.get_status()}")

    # 模拟战斗
    print(f"\n⚔️ 战斗开始:")

    # 第一轮攻击
    warrior.attack(mage)
    mage.attack(warrior)

    # 使用技能
    print(f"\n🔮 使用技能:")
    warrior.use_skill("狂暴", SkillType.BUFF)
    mage.use_skill("治疗术", SkillType.HEAL)

    # 狂暴状态下攻击
    print(f"\n😡 狂暴攻击:")
    warrior.attack(mage)
    warrior.attack(mage)

    # 模拟时间流逝
    print(f"\n⏰ 时间流逝...")
    for i in range(10):
        warrior.update(1.0)
        mage.update(1.0)
        time.sleep(0.1)

    print(f"\n📊 战斗后状态:")
    print(f"   {warrior.get_status()}")
    print(f"   {mage.get_status()}")


if __name__ == "__main__":
    demo_character_states()

    print("\n" + "=" * 60)
    print("✅ 游戏角色状态演示完成")
    print("💡 学习要点:")
    print("   - 状态影响角色的行为能力")
    print("   - 状态间的自动转换机制")
    print("   - 状态的持续时间管理")
    print("   - 状态对数值的修正效果")
    print("=" * 60)
